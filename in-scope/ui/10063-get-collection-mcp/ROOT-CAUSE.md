# pid 10063 — set_variable does not reapply write-through bindings

## Root cause
Bindings are write-through: the resolved value is copied into the node's own field (`applyBoundVariablesToNode`, `packages/core/src/scene-graph/variables.ts:539-605`, `record[key] = value` at :602). `bindVariable` runs this at bind time (variables.ts:767), so `node.opacity` = value-at-bind (0.3).

`setVariableValue` updates only `valuesByMode` and never reapplies bindings:
`packages/core/src/figma-api/index.ts:359-363`
```ts
setVariableValue(variableId, modeId, value) {
  const variable = this.graph.variables.get(variableId)
  if (!variable) throw new Error(...)
  variable.valuesByMode[modeId] = value
}
```
Contrast `setVariableMode` (index.ts:377-387) which DOES call `this.graph.applyAllBoundVariables()` (:386).

`get_node` reports the stored scalar (`serialization.ts:86`); the live value is reported separately as `boundVariables.opacity.resolvedValue` (`serialization.ts:7-19`). Hence 0.3 vs 0.9.

## Proposed fix
`setVariableValue` should call `this.graph.applyAllBoundVariables()` after mutating `valuesByMode`, mirroring `setVariableMode`.

## Acceptance criteria
- After `set_variable`, `get_node` opacity equals the new resolved value; scalar and resolvedValue agree.

## Disposition
APP BUG — filed RLCU-2654. Task cannot pass reliably until the app fix ships. No task/prompt change; staged for retest post-deploy.
