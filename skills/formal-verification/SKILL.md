---
name: formal-verification
description: Generate a project-local skill that formally verifies the code where a bug costs the most and tests reach the least, in any language, with whichever verification tool fits. Use when asked to formally verify code, model-check a race or state machine, prove an invariant, or when concurrency, reactive graphs, retries, state machines, parsers, or security boundaries need exhaustive verification beyond example-based unit tests.
---

# Create a formal verification skill

A test checks the cases that someone thought to write. Formal verification checks every case in a stated scope: every order of steps in a model, every state transition up to a bound, or every input within a domain. This skill finds the part of the repo where that matters most, verifies one or more high-consequence properties of it, and saves a project-local skill (in `.agents/skills/<name>/SKILL.md` or the agent's skill store) that lets the next agent check a change against that property. Write that skill for an agent who reads it cold, mid-change, and has never seen your work. The user must be able to trust the result and act on it without learning a specialized verification language.

## Choose the target from the code

Answer from the codebase, and ask the user only what you cannot observe. If the user named an area or a bug, start there.

A good target is a promise the code makes, where a break harms users and example-based tests rarely reach the case that breaks it. Choose the strongest such target in the repo, not the one that is easiest to verify.

## Let the question choose the tool

Pick the tool that answers the question at the lowest cost: a state-space model checker, an exhaustive bounded verifier, an SMT-backed verifier, or property-based exhaustive enumeration on the real code.
- Whether events or transitions can happen in a bad order suits a state-machine or state-space model checker over a faithful model or direct driver of the design (for example, TLA+ when available, or an exhaustive BFS/DFS state-space explorer in the project's native runtime).
- Whether the code itself behaves for every input, such as reactive DAG glitch freedom, parser termination, tree depth/budget bounds, or a data-structure invariant, suits a verifier that runs directly on the real code over all inputs up to a stated bound.
- Prefer a tool that runs in one command with the repo's existing toolchain (`node`, `python3`, `cargo`, `go`, etc.), and tell the user why you chose it.

## What makes it good

- **True to the code.** Every part of the model or proof points to code that a reviewer can open. What the verification treats as one indivisible step is one indivisible step in the code. Names come from this repo.
- **Able to fail.** A check that you have never seen fail proves nothing. Show each property failing on a broken variant of the code it guards, such as a removed check or a reordered step.
- **Findings stay findings.** When the current code breaks the property, report it with the counterexample in the code's terms. Do not weaken the property or the model until it passes, and do not change product code unless the user asks.
- **Honest about scope.** Say what is verified, under which bounds and assumptions, and what is left out. A pass covers the model or the bound, not the whole system.
- **Readable without the tool.** State the property and the harm in one plain sentence each. Tell a counterexample as a short sequence of steps in the code's words.
- **Cheap to rerun.** One command, a reproducible tool version, and a run short enough that the next agent will use it on every relevant change.
- **Kept in step with the code.** Record which files and functions each check covers, and the commit at which you last confirmed that the verification describes them. When the covered code changes after that commit, the next agent can see that the verification needs another look.

## Generate the verify skill

From the generated skill alone, the next agent must be able to:
1. Tell whether a change touches the verified code.
2. Run the verification check in a single command.
3. Tell a real bug from a modeling error.
4. Update the verification when a change is intended.

Put the coverage record (covered files/functions) and the sync commit SHA in the skill, and instruct the next agent to move the sync commit forward only after confirming that the verification accurately describes the code at the new commit. Use the repo's real commands, paths, and nouns, and leave no placeholders.

## Prove it before you hand off

Follow the generated skill once, as the next agent would, on a scratch change or mutation that breaks the property in the real code. It must catch the break and print a minimal counterexample. Then restore the code and confirm that the check is back where it started: passing, or failing only on the findings you will report. A verify skill that was never run is a draft. If the skill misses the break or a step does not run, fix the skill or the verification, not the scratch change.

## Hand off

Tell the user what you verified, which tool or approach you used and why, the bounds, what the check found in plain words, how to run it, and what it does not cover. Suggest a second target only if you found a close one.
