# policy

RuleOak Python guide for policy. Examples are offline and do not require optional frameworks. Contact: hello@ruleoak.com.

## Policy precedence

RuleOak Python Bridge follows the RuleOak policy model:

1. `blockedActions` always wins.
2. `allowedActions` and `approvalRequired` are compared by pattern specificity.
3. If allow and approval match with the same specificity, `needs_approval` wins.
4. `defaultAction` applies only when no explicit policy pattern matches.

Exact patterns such as `filesystem.read` are more specific than `filesystem.*`, and `*` is the least-specific catch-all. This supports broad approval defaults with precise safe exceptions.
