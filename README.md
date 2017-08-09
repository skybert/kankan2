# kankan2 👁 - Easy integration tests - 看看

Easy integration tests using Python3

## Example output

```
$ ./kankan2
Tests: 2 Successes: 1 Errors: 1
  File "./kankan2", line 19, in run_check
    check(conf)
  File "/home/torstein/src/kankan2/checks/area_teaser_options_placement_VF_7149.py", line 91, in check
    check_teaser_options(doc, "main-area-items-option-size")
  File "/home/torstein/src/kankan2/checks/area_teaser_options_placement_VF_7149.py", line 71, in check_teaser_options
    assert len(r) > 0
```

## What's in a name
`kankan` is Chinese for `look`, or `check` (it out). The Chinese
characters are 看看.

