// autoresearch-safe: test-vector policy for agent-governance-testvectors.
//
// Evaluates tool calls typical of a research / development agent.
// Covers four cases: allow Read, allow safe Bash, deny destructive Bash,
// deny unscoped Write.

// Allow read-oriented tools.
permit (
    principal,
    action in [Action::"Read", Action::"Glob", Action::"Grep", Action::"WebSearch"],
    resource
);

// Allow Bash for a safe command list only. Set membership on a string is
// .contains(); `in` is the entity-hierarchy operator and a string on its
// left is a type error in Cedar (found 2026-09-10 with cedar-wasm).
permit (
    principal,
    action == Action::"Bash",
    resource
) when {
    ["git", "npm", "ls", "cat", "pwd", "echo", "node", "python"].contains(context.command_pattern)
};

// Deny destructive Bash regardless of any permit.
// Cedar forbid is authoritative.
forbid (
    principal,
    action == Action::"Bash",
    resource
) when {
    ["rm -rf", "dd", "mkfs", "shred"].contains(context.command_pattern)
};

// Writes must be within the project directory.
permit (
    principal,
    action in [Action::"Write", Action::"Edit"],
    resource
) when {
    context.path_starts_with == "./"
};
