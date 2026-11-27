# Diagram views for the design decision

Start with an **architecture map** for the representative flow. Mark the
consumers of each shared part and where the authoritative outcome lives. Label significant
arrows with the contract, data or action crossing them. Keep dependency arrows
distinct from runtime calls. Use a separate view when the meaning would mix.

Add a view when it answers a decision the map cannot:

| Question | View |
|---|---|
| Where does an outcome change after failure or retry? | Sequence or state machine covering that transition. |
| What can two consumers reuse or extend? | A dependency view with the shared interface and its consumers. Indicate where feature-specific state stays. |
| What changes in an existing system? | Before/after architecture delta. Show the current path and the proposed path or migration seam. |
| What persists, runs or crosses a trust boundary? | Data, deployment or dependency view for the risk in question. |

Give every view a caption stating the scope, source and evidence status. Split
observed, reported and proposed paths when a reader could mistake one for
another. For takeover, draw discrepancies visibly. A workbook's network path,
a local fixture path and a deployed path with no evidence are three different
claims. Identify the unknown owner or boundary on the drawing.

Keep editable diagram source next to the decision or embed Mermaid in the
review note. If `diagram-design` is available, use its workflow where a
rendered diagram would aid review. On a harness without that capability,
deliver the Mermaid source in the note. Quote flowchart labels containing
syntax characters such as parentheses and brackets. In sequence messages,
use plain sentences instead of Mermaid statement separators such as
semicolons. Check the rendered view
or parse the source when a renderer or parser is available. Otherwise check
the syntax by inspection. Read the drawing against the flow and its evidence.
