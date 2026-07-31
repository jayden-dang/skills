# 0007 — The dogfood server is agent-managed, and stops only on proof of identity

`dogfood serve` is a background process an agent starts, which is the largest **ARCH-3**
friction this skill set has taken on: every other enforcement mechanism here is a `grep`, a
`git` call, or a file read, and this one is a daemon holding a port. **Decision:** accept it,
bounded — the server binds loopback only, every other subcommand works fully without it
(**ARCH-2**), and `serve --stop` terminates a process only when `/whoami` on the recorded port
answers with the token written in the pidfile, deleting a stale pidfile and killing nothing
otherwise. **Why:** the alternative of a foreground server the person starts was offered and
declined in favour of the agent starting it, which turns orphan processes from an accident
into a normal operating state that must be designed for; and a plain pidfile checked with
`kill -0` is not adequate for that, because `kill -0` answers "does this PID exist", which is
exactly what stays true after the operating system recycles the PID onto an unrelated
process — so the cheap version buys about fifteen lines at the price of occasionally killing
something that was never ours. Recording the friction rather than smoothing it over is the
point: a future reader weighing another background surface should find the cost stated here,
not rediscover it.
