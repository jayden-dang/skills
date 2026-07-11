# Standards Baseline

Twelve smells the Standards axis always checks, even in a repo that documents
nothing. Every hit is a labeled judgment call ("possible feature envy"), never
a hard violation; a documented repo standard overrides any item here; skip
anything the repo's tooling already enforces.

Each entry: **what it is → how to fix.**

1. **Duplicated knowledge** — one fact or rule (a formula, a validation, a
   mapping) encoded in two or more places in the diff, so a future change must
   find every copy. → Extract the single source of truth and make every site
   consume it.

2. **Shallow module** — a class, function, or file whose interface is nearly
   as complicated as what it hides; callers gain nothing by going through it.
   → Deepen it (pull real logic behind the interface) or delete it and let
   callers do the work directly.

3. **Leaky abstraction** — an interface that forces callers to know about its
   internals: exposed storage shapes, required call orderings, error types
   from three layers down. → Redesign the boundary so the caller can stay
   ignorant of the implementation.

4. **Feature envy** — a function that spends its time reading and picking
   apart another module's data rather than its own. → Move the behavior onto
   the module that owns the data.

5. **Long parameter list** — a signature taking so many arguments (or several
   that always travel together) that call sites become unreadable and
   error-prone. → Bundle the co-traveling values into one named type, or let
   the function fetch what it can derive.

6. **Dead code** — functions, branches, flags, or exports the diff adds or
   keeps that nothing reaches. → Delete it; version control remembers.

7. **Speculative generality** — abstraction, hooks, or parameters added for
   needs no requirement has: "we might need it later". → Remove it and inline
   until a real caller shows up.

8. **Shotgun surgery** — one logical change in the diff forcing small edits
   scattered across many files. → Gather the pieces that change together into
   one module so the next change lands in one place.

9. **Primitive obsession** — a bare string, number, or map standing in for a
   domain concept (an ID, a money amount, a state) that deserves its own type
   with its own rules. → Introduce the small domain type and move the
   validation into it.

10. **Mysterious name** — an identifier that hides what it does or holds
    (`data2`, `process`, `handleStuff`), or one that describes the mechanism
    instead of the purpose. → Rename to what it means; if no honest name
    exists, the design underneath is the problem.

11. **Comment compensating for bad code** — a comment that explains WHAT
    confusing code does, papering over structure that should explain itself.
    → Refactor until the comment is unnecessary; keep comments that explain
    WHY (constraints, trade-offs, gotchas).

12. **Inconsistent vocabulary** — the same concept under different names
    across the diff (or a name that contradicts CONTEXT.md's glossary), so
    readers must guess whether two terms are one thing. → Pick the repo's
    canonical term and use it everywhere; update CONTEXT.md if the term is
    genuinely new.

## Security — when the diff touches a trust boundary

The twelve above are quality smells; these are the security concerns the
Standards axis raises whenever the diff crosses a trust boundary — anywhere
untrusted input enters, a secret is handled, or a privileged action is taken.
Same rules as above: each is a labeled judgment call, a documented repo standard
or an existing scanner overrides it, and skip what tooling already enforces. When
the diff touches none of these boundaries, say so and move on — do not
manufacture findings.

13. **Injection** — untrusted input concatenated into a SQL query, shell
    command, HTML/DOM, template, or file path, so the input can change the
    command's structure. → Use parameterized queries, safe argument arrays,
    context-aware escaping, or an allow-list; never string-build the command.

14. **Broken authz / missing access check** — an endpoint, handler, or query
    that acts on a resource without confirming the caller is authenticated AND
    allowed to touch *that specific* resource (the classic IDOR: trusting an ID
    from the request). → Enforce the check server-side at the boundary, scoped
    to the caller.

15. **Secret exposure** — a credential, token, or key hard-coded in the diff,
    logged, returned in an error/response, or committed to config. → Read it
    from the environment or a secret store; keep it out of source, logs, and
    responses; rotate anything that landed in history.

16. **Unvalidated input reaching a sink** — request data used as a size, index,
    redirect target, deserialization payload, or outbound URL (SSRF) without
    validation. → Validate type, range, and shape at the boundary; allow-list
    redirect and fetch targets; never deserialize untrusted data into live
    objects.

17. **Sensitive data in the clear** — PII, secrets, or auth material stored or
    transmitted without encryption, or hashed passwords using a fast/plain
    digest instead of a slow salted KDF. → Encrypt in transit and at rest; use
    a purpose-built password hash (argon2/bcrypt/scrypt).

18. **Weak or misused crypto / randomness** — a non-cryptographic RNG for a
    token, password reset, or session ID; a home-rolled or deprecated
    algorithm; a missing signature/nonce check. → Use the platform's vetted
    crypto and CSPRNG; verify signatures and reject replays.
