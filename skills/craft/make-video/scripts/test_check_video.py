#!/usr/bin/env python3
"""Run with: python3 -m unittest discover -s skills/craft/make-video/scripts"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import check_video as cv  # noqa: E402


def script(**over):
    base = {
        "language": "en",
        "source": {"kind": "feature", "ref": "abc123"},
        "scenes": [
            {"id": "a", "kind": "points", "title": "T", "points": ["p"], "beats": [{"text": "One line.", "ref": "alerts.js:3"}]}
        ],
    }
    base.update(over)
    return base


class ValidateScript(unittest.TestCase):
    def test_a_complete_script_has_no_faults(self):
        self.assertEqual(cv.validate_script(script()), [])

    def test_a_sentence_without_a_source_is_a_fault(self):
        s = script()
        s["scenes"][0]["beats"][0]["ref"] = ""
        self.assertIn("a-0: no source", cv.validate_script(s))

    def test_a_sentence_over_twenty_words_is_a_fault(self):
        s = script()
        s["scenes"][0]["beats"][0]["text"] = " ".join(["word"] * 21)
        self.assertIn("a-0: over 20 words", cv.validate_script(s))

    def test_vietnamese_counts_syllables_so_it_gets_more_tokens(self):
        s = script(language="vi")
        s["scenes"][0]["beats"][0]["text"] = " ".join(["từ"] * 30)
        self.assertEqual(cv.validate_script(s), [])
        s["scenes"][0]["beats"][0]["text"] = " ".join(["từ"] * 31)
        self.assertIn("a-0: over 30 words", cv.validate_script(s))

    def test_an_unknown_source_kind_is_a_fault(self):
        self.assertIn("source.kind must be feature, pr, release, spec or concept", cv.validate_script(script(source={"kind": "pitch", "ref": "x"})))

    def test_a_missing_language_is_a_fault(self):
        s = script()
        del s["language"]
        self.assertIn("language is missing", cv.validate_script(s))

    def test_a_clip_scene_with_no_clip_is_a_fault(self):
        s = script()
        s["scenes"][0] = {"id": "c", "kind": "clip", "title": "T", "beats": [{"text": "Hi.", "ref": "a.js:1"}]}
        self.assertIn("c: clip scene names no clip", cv.validate_script(s))


REQUIREMENTS = """# Requirements: Rebooking
## 1. Offer
- **REBOOK-1.1** WHEN staff cancel THE SYSTEM SHALL offer.
- **REBOOK-1.2** THE SYSTEM SHALL pick the next sailing.
## 2. Hold
- **REBOOK-2.1** THE SYSTEM SHALL hold a seat.
- ~~**REBOOK-2.2**~~ retired.
"""


def spec_script(**over):
    base = {
        "language": "en",
        "planned": "Planned, not built",
        "source": {"kind": "spec", "ref": "abc123", "spec": "docs/specs/rebooking"},
        "scenes": [
            {"id": "world", "kind": "world", "title": "T", "beats": [
                {"text": "Lan has a seat on the ferry.", "ref": "REBOOK-1.1"},
                {"text": "It is cancelled, so she needs another.", "ref": "REBOOK-1.2"},
                {"text": "But the seat could go, so it is held.", "ref": "REBOOK-2.1"},
            ]},
        ],
    }
    base.update(over)
    return base


def beats(*texts):
    return [{"text": t, "ref": "REBOOK-1.1"} for t in texts]


class SpecFilm(unittest.TestCase):
    def test_an_explanation_has_no_faults(self):
        self.assertEqual(cv.judge_spec(spec_script(), REQUIREMENTS), [])

    def test_a_story_it_does_not_tell_is_no_fault(self):
        s = spec_script()
        s["scenes"][0]["beats"] = beats("So this.", "Because that.", "But then.")
        self.assertEqual(cv.judge_spec(s, REQUIREMENTS), [])

    def test_an_id_the_spec_does_not_define_is_a_fault(self):
        s = spec_script()
        s["scenes"][0]["beats"][0]["ref"] = "REBOOK-9.9"
        self.assertIn("REBOOK-9.9 is not in requirements.md", cv.judge_spec(s, REQUIREMENTS))

    def test_a_retired_id_is_a_fault(self):
        s = spec_script()
        s["scenes"][0]["beats"][0]["ref"] = "REBOOK-2.2"
        self.assertIn("REBOOK-2.2 is not in requirements.md", cv.judge_spec(s, REQUIREMENTS))

    def test_footage_is_a_fault_because_nothing_is_built(self):
        s = spec_script()
        s["scenes"].append({"id": "shot", "kind": "clip", "title": "T", "beats": beats("So a clip.")})
        self.assertIn("shot: a spec film shows no footage", cv.judge_spec(s, REQUIREMENTS))

    def test_a_second_bullet_scene_is_a_fault(self):
        s = spec_script()
        for name in ("one", "two"):
            s["scenes"].append({"id": name, "kind": "points", "title": "T", "points": ["p"], "beats": beats("So this, because that.")})
        self.assertIn("2 points scenes: a spec film has at most 1", cv.judge_spec(s, REQUIREMENTS))

    def test_a_film_with_no_world_is_a_fault(self):
        s = spec_script()
        s["scenes"][0]["kind"] = "table"
        self.assertIn("no world scene", cv.judge_spec(s, REQUIREMENTS))

    def test_a_list_of_facts_is_a_fault(self):
        s = spec_script()
        s["scenes"][0]["beats"] = beats("Then offers.", "The sweep.", "The routes.", "So it ends.")
        self.assertIn("1 of 4 lines give a reason; an explanation needs a third", cv.judge_spec(s, REQUIREMENTS))

    def test_reasons_count_in_vietnamese(self):
        s = spec_script(language="vi")
        s["scenes"][0]["beats"] = beats("Nên cửa sổ mở ra.", "Hết giờ.", "Vì vậy ghế được giữ.")
        self.assertEqual(cv.judge_spec(s, REQUIREMENTS), [])
        s["scenes"][0]["beats"] = beats("Kế hoạch.", "Hết giờ.", "Năm task.")
        self.assertIn("0 of 3 lines give a reason; an explanation needs a third", cv.judge_spec(s, REQUIREMENTS))

    def test_a_language_with_no_word_list_is_not_judged_on_reasons(self):
        s = spec_script(language="de")
        s["scenes"][0]["beats"] = beats("Eins.", "Zwei.", "Drei.")
        self.assertEqual(cv.judge_spec(s, REQUIREMENTS), [])

    def test_no_planned_label_is_a_fault(self):
        s = spec_script()
        del s["planned"]
        self.assertIn("planned label is missing", cv.judge_spec(s, REQUIREMENTS))

    def test_no_spec_folder_is_a_fault(self):
        s = spec_script()
        del s["source"]["spec"]
        self.assertIn("source.spec is missing", cv.validate_script(s))

    def test_it_lists_what_the_film_leaves_out_in_order(self):
        s = spec_script()
        s["scenes"][0]["beats"] = beats("One.")
        reqs = REQUIREMENTS + "- **REBOOK-1.10** THE SYSTEM SHALL.\n"
        self.assertEqual(cv.uncited(s, reqs), ["REBOOK-1.2", "REBOOK-1.10", "REBOOK-2.1"])


DESIGN = """# Design
```js
type Offer = {
  token: string;
};
```
"""


class SpecQuotes(unittest.TestCase):
    def read(self, path):
        return {"docs/specs/rebooking/design.md": DESIGN, "docs/specs/rebooking/requirements.md": REQUIREMENTS}.get(path)

    def quoting(self, scene):
        return spec_script(scenes=[scene])

    def test_a_rule_in_the_spec_words_passes(self):
        s = self.quoting({"id": "r", "kind": "ears", "rules": [{"id": "REBOOK-1.2", "text": "THE SYSTEM SHALL pick the next sailing."}], "beats": []})
        self.assertEqual(cv.judge_quotes(s, self.read), [])

    def test_a_reworded_rule_is_a_fault(self):
        s = self.quoting({"id": "r", "kind": "ears", "rules": [{"id": "REBOOK-1.2", "text": "THE SYSTEM SHALL choose a sailing."}], "beats": []})
        self.assertIn("r: REBOOK-1.2 is not in the spec's words", cv.judge_quotes(s, self.read))

    def test_code_from_the_file_passes(self):
        s = self.quoting({"id": "c", "kind": "code", "file": "docs/specs/rebooking/design.md", "lines": ["type Offer = {", "  token: string;", "};"], "beats": []})
        self.assertEqual(cv.judge_quotes(s, self.read), [])

    def test_code_the_file_does_not_hold_is_a_fault(self):
        s = self.quoting({"id": "c", "kind": "code", "file": "docs/specs/rebooking/design.md", "lines": ["type Offer = {", "  id: number;"], "beats": []})
        self.assertIn("c: line 2 is not in docs/specs/rebooking/design.md", cv.judge_quotes(s, self.read))

    def test_code_from_a_file_that_is_not_there_is_a_fault(self):
        s = self.quoting({"id": "c", "kind": "code", "file": "offers.js", "lines": ["x"], "beats": []})
        self.assertIn("c: offers.js is not at the pinned commit", cv.judge_quotes(s, self.read))


def world(objects, beats):
    return {"scenes": [{"id": "w", "kind": "world", "title": "T", "objects": objects, "beats": beats}]}


def box(id, x, y, w, h, **more):
    return {"id": id, "shape": "card", "x": x, "y": y, "w": w, "h": h, **more}


def showing(**world_change):
    return {"text": "A line.", "ref": "x", "world": world_change}


class WorldCamera(unittest.TestCase):
    def test_a_camera_holding_all_it_shows_has_no_faults(self):
        s = world([box("a", 100, 100, 200, 100)], [showing(set={"a": {}}, camera={"x": 0, "y": 0, "w": 900, "h": 420})])
        self.assertEqual(cv.judge_world(s), [])

    def test_a_thing_cut_by_the_camera_is_a_fault(self):
        s = world([box("late", 800, 100, 400, 100)], [showing(set={"late": {}}, camera={"x": 0, "y": 0, "w": 900, "h": 420})])
        self.assertIn("w-0: late is cut by the camera", cv.judge_world(s))

    def test_a_thing_wholly_out_of_frame_is_no_fault(self):
        s = world([box("far", 3000, 100, 200, 100)], [showing(set={"far": {}}, camera={"x": 0, "y": 0, "w": 900, "h": 420})])
        self.assertEqual(cv.judge_world(s), [])

    def test_a_hidden_thing_is_no_fault(self):
        s = world([box("a", 800, 100, 400, 100)], [showing(camera={"x": 0, "y": 0, "w": 900, "h": 420})])
        self.assertEqual(cv.judge_world(s), [])

    def test_a_background_filling_the_frame_is_no_fault(self):
        s = world([box("desk", 0, 0, 1800, 840)], [showing(set={"desk": {}}, camera={"x": 100, "y": 100, "w": 900, "h": 420})])
        self.assertEqual(cv.judge_world(s), [])

    def test_the_default_camera_is_the_whole_world(self):
        s = world([box("wide", 1700, 100, 200, 100)], [showing(set={"wide": {}})])
        self.assertIn("w-0: wide is cut by the camera", cv.judge_world(s))

    def test_a_camera_carries_over_and_a_later_move_is_judged(self):
        s = world([box("a", 100, 100, 200, 100)], [
            showing(set={"a": {}}, camera={"x": 0, "y": 0, "w": 900, "h": 420}),
            showing(set={"a": {"x": 800}}),
        ])
        self.assertIn("w-1: a is cut by the camera", cv.judge_world(s))

    def test_a_change_part_way_through_a_line_is_judged(self):
        s = world([box("a", 100, 100, 200, 100), box("b", 800, 100, 400, 100)], [
            showing(set={"a": {}}, camera={"x": 0, "y": 0, "w": 900, "h": 420}, then=[{"at": "Second", "set": {"b": {}}}]),
        ])
        self.assertIn("w-0: b is cut by the camera", cv.judge_world(s))

    def test_a_frame_wider_than_its_camera_shows_more_than_the_box(self):
        # A tall camera box is letterboxed, so the frame is wider than the box that asked for it.
        s = world([box("a", 300, 100, 200, 100)], [showing(set={"a": {}}, camera={"x": 0, "y": 0, "w": 370, "h": 370})])
        self.assertEqual(cv.judge_world(s), [])

    def test_one_cut_thing_reports_once_while_the_camera_holds(self):
        s = world([box("a", 800, 100, 400, 100)], [
            showing(set={"a": {}}, camera={"x": 0, "y": 0, "w": 900, "h": 420}),
            showing(),
        ])
        self.assertEqual(cv.judge_world(s), ["w-0: a is cut by the camera"])


class ScriptFaults(unittest.TestCase):
    def test_it_judges_a_script_with_no_film(self):
        s = script()
        s["scenes"][0]["beats"][0]["ref"] = ""
        self.assertIn("a-0: no source", cv.script_faults(s, "."))

    def test_it_judges_a_world_camera(self):
        s = script()
        s["scenes"] = world([box("wide", 1700, 100, 200, 100)], [showing(set={"wide": {}})])["scenes"]
        self.assertIn("w-0: wide is cut by the camera", cv.script_faults(s, "."))


class SpecLength(unittest.TestCase):
    def test_every_spec_gets_two_minutes(self):
        self.assertEqual(cv.judge_length(120.0), [])

    def test_over_two_minutes_is_a_fault(self):
        self.assertIn("120.5s is over the 120s limit", cv.judge_length(120.5))


def concept(**over):
    base = {
        "language": "en",
        "source": {"kind": "concept", "topic": "Raft leader election"},
        "sources": [{"id": "raft-5.2", "cite": "Ongaro and Ousterhout 2014, In Search of an Understandable Consensus Algorithm, section 5.2"}],
        "scenes": [
            {"id": "elect", "kind": "manim", "title": "An election", "beats": [
                {"text": "A follower hears nothing, so it starts an election.", "ref": "raft-5.2"},
                {"text": "It votes for itself because it wants to lead.", "ref": "raft-5.2"},
            ]}
        ],
    }
    base.update(over)
    return base


class Concept(unittest.TestCase):
    def test_a_concept_film_with_sources_has_no_faults(self):
        self.assertEqual(cv.judge_concept(concept()), [])

    def test_a_concept_needs_no_commit(self):
        self.assertEqual(cv.validate_script(concept()), [])

    def test_no_sources_is_a_fault(self):
        self.assertIn("sources is missing: a concept film lists each source as {id, cite}", cv.judge_concept(concept(sources=[])))

    def test_a_ref_to_no_listed_source_is_a_fault(self):
        s = concept()
        s["scenes"][0]["beats"][0]["ref"] = "the Raft paper"
        self.assertIn("elect-0: ref names no source in sources and no file:line", cv.judge_concept(s))

    def test_a_source_id_inside_another_word_does_not_count(self):
        s = concept()
        s["scenes"][0]["beats"][0]["ref"] = "raft-5.2x"
        self.assertIn("elect-0: ref names no source in sources and no file:line", cv.judge_concept(s))

    def test_a_file_and_line_counts_as_a_source(self):
        s = concept()
        s["scenes"][0]["beats"][0]["ref"] = "src/raft.rs:40"
        self.assertEqual(cv.judge_concept(s), [])

    def test_a_concept_film_that_draws_nothing_is_a_fault(self):
        s = concept()
        s["scenes"][0]["kind"] = "points"
        self.assertIn("no manim or world scene: a concept film draws the idea", cv.judge_concept(s))

    def test_a_concept_film_explains(self):
        s = concept()
        for b in s["scenes"][0]["beats"]:
            b["text"] = "A follower starts an election."
        self.assertIn("0 of 2 lines give a reason; an explanation needs a third", cv.judge_concept(s))

    def test_a_concept_film_may_run_five_minutes(self):
        self.assertEqual(cv.judge_length(300.0, cv.CONCEPT_MAX), [])
        self.assertIn("300.5s is over the 300s limit", cv.judge_length(300.5, cv.CONCEPT_MAX))

    def test_an_unrendered_manim_scene_is_a_fault(self):
        self.assertIn("elect: public/manim/elect.webm is missing; run render_manim.py", cv.judge_manim_renders(concept(), "/nonexistent"))

    def test_a_feature_film_still_needs_a_commit(self):
        self.assertIn("source.ref is missing", cv.validate_script(script(source={"kind": "feature"})))


class JudgeClip(unittest.TestCase):
    def test_sixteen_by_nine_at_1600_passes(self):
        self.assertIsNone(cv.judge_clip(1600, 900))

    def test_the_default_recorded_viewport_fails(self):
        self.assertIn("1280x578", cv.judge_clip(1280, 578))

    def test_small_sixteen_by_nine_fails(self):
        self.assertIn("1280x720", cv.judge_clip(1280, 720))


class JudgeMedia(unittest.TestCase):
    def clean(self, **over):
        m = {"width": 1920, "height": 1080, "has_audio": True, "duration": 60.0, "peak": -2.0, "loudness": -16.0, "freezes": [], "silences": []}
        m.update(over)
        return m

    def test_a_clean_render_has_no_faults(self):
        self.assertEqual(cv.judge_media(self.clean()), [])

    def test_720p_fails(self):
        self.assertTrue(any("1920x1080" in f for f in cv.judge_media(self.clean(width=1280, height=720))))

    def test_no_audio_fails(self):
        self.assertIn("no audio stream", cv.judge_media(self.clean(has_audio=False)))

    def test_a_long_still_mid_video_fails(self):
        faults = cv.judge_media(self.clean(freezes=[(10.0, 8.0)]))
        self.assertTrue(any("still for 8.0s at 10.0s" in f for f in faults))

    def test_a_still_closing_card_passes(self):
        self.assertEqual(cv.judge_media(self.clean(freezes=[(52.0, 8.0)])), [])

    def test_a_long_silence_mid_video_fails(self):
        faults = cv.judge_media(self.clean(silences=[(20.0, 3.5)]))
        self.assertTrue(any("silent for 3.5s at 20.0s" in f for f in faults))

    def test_a_clipping_peak_fails(self):
        self.assertTrue(any("peak" in f for f in cv.judge_media(self.clean(peak=-0.3))))


class FileRefs(unittest.TestCase):
    def test_finds_path_and_line(self):
        self.assertEqual(cv.file_refs("alerts.js:3, docs/a.md:12 and a request"), [("alerts.js", 3), ("docs/a.md", 12)])

    def test_ignores_text_without_a_line(self):
        self.assertEqual(cv.file_refs("recorded run, GET /health"), [])


class SheetFilter(unittest.TestCase):
    def test_named_frames_are_the_ones_selected(self):
        vf = cv.sheet_filter([12, 40, 95], 30.0)
        self.assertIn(r"select='eq(n\,12)+eq(n\,40)+eq(n\,95)'", vf)
        self.assertIn("tile=4x1", vf)

    def test_rows_grow_with_the_lines(self):
        self.assertIn("tile=4x3", cv.sheet_filter(list(range(9)), 30.0))

    def test_without_named_frames_it_samples_evenly(self):
        vf = cv.sheet_filter(None, 48.0)
        self.assertIn("fps=1/3.0", vf)
        self.assertIn("tile=4x4", vf)
        self.assertNotIn("select", vf)


class Pace(unittest.TestCase):
    def film(self, *lines, language="en"):
        return {"language": language, "scenes": [{"id": "w", "kind": "world", "objects": [], "beats": list(lines)}]}

    def line(self, words, **world):
        return {"text": " ".join(f"w{i}" for i in range(words)), "ref": "x", "world": world}

    def test_a_short_line_with_a_change_passes(self):
        self.assertEqual(cv.judge_pace(self.film(self.line(9, set={"a": {}}))), [])

    def test_a_long_line_with_one_change_is_a_fault(self):
        self.assertEqual(cv.judge_pace(self.film(self.line(20, set={"a": {}}))), ["w-0: 20 words with nothing changing"])

    def test_a_change_part_way_breaks_the_run(self):
        self.assertEqual(cv.judge_pace(self.film(self.line(18, set={"a": {}}, then=[{"at": "w9", "set": {"b": {}}}]))), [])

    def test_a_late_change_leaves_the_long_run_before_it(self):
        self.assertEqual(cv.judge_pace(self.film(self.line(20, set={"a": {}}, then=[{"at": "w15", "set": {"b": {}}}]))), ["w-0: 15 words with nothing changing"])

    def test_a_line_that_changes_nothing_is_a_fault(self):
        self.assertEqual(cv.judge_pace(self.film(self.line(5))), ["w-0: nothing changes on this line"])

    def test_vietnamese_counts_syllables(self):
        self.assertEqual(cv.judge_pace(self.film(self.line(14, set={"a": {}}), language="vi")), [])
        self.assertEqual(cv.judge_pace(self.film(self.line(15, set={"a": {}}), language="vi")), ["w-0: 15 words with nothing changing"])

    def test_a_change_at_words_the_line_does_not_say_is_a_fault(self):
        self.assertEqual(cv.judge_pace(self.film(self.line(5, set={"a": {}}, then=[{"at": "nobody said", "set": {"b": {}}}]))), ['w-0: "nobody said" is not in the line'])

    def test_changes_must_run_forward(self):
        self.assertEqual(cv.judge_pace(self.film(self.line(9, set={"a": {}}, then=[{"at": "w6", "set": {"b": {}}}, {"at": "w3", "set": {"c": {}}}]))), ['w-0: "w3" comes before the change above it'])

    def test_the_phrase_may_span_words_and_ignores_case_and_commas(self):
        line = {"text": "Lan waits, so The Seat holds.", "ref": "x", "world": {"set": {"a": {}}, "then": [{"at": "so the seat", "set": {"b": {}}}]}}
        self.assertEqual(cv.judge_pace(self.film(line)), [])

    def test_only_a_world_is_paced(self):
        s = {"language": "en", "scenes": [{"id": "p", "kind": "points", "beats": [self.line(20)]}]}
        self.assertEqual(cv.judge_pace(s), [])


class Holds(unittest.TestCase):
    def test_runs_of_small_change_become_spans(self):
        self.assertEqual(cv.hold_spans([500, 3, 3, 3, 500, 3], fps=1), [(1, 3), (5, 1)])

    def test_a_label_changing_is_not_a_hold_and_a_moving_dot_is(self):
        self.assertEqual(cv.hold_spans([cv.STILL_PIXELS + 1], fps=1), [])
        self.assertEqual(cv.hold_spans([cv.STILL_PIXELS - 1], fps=1), [(0, 1)])

    def test_changed_pixels_come_from_the_share_of_a_binary_plane(self):
        self.assertEqual(cv.changed_pixels("lavfi.signalstats.YAVG=255\nlavfi.signalstats.YAVG=0\n"), [cv.STILL_AREA, 0])

    def test_the_closing_line_may_rest(self):
        m = {"width": 1920, "height": 1080, "has_audio": True, "peak": -3, "duration": 60, "freezes": [(52, 7.0)], "silences": []}
        self.assertEqual(cv.judge_media(m, max_still=4.5), [])

    def test_a_hold_is_judged_against_the_limit_given(self):
        m = {"width": 1920, "height": 1080, "has_audio": True, "peak": -3, "duration": 60, "freezes": [(10, 4.0)], "silences": []}
        self.assertEqual(cv.judge_media(m), [])
        self.assertEqual(cv.judge_media(m, max_still=3.0), ["still for 4.0s at 10.0s"])


if __name__ == "__main__":
    unittest.main()
