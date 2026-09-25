# Filtering load test

<!-- toc:start -->
**Table of contents**

- [Filtering load test](#filtering-load-test)
<!-- toc:end -->

[Theory and conditions](<../../docs/adaptive-filtering/README.md#computational-cost>)

A gate is a template `if` condition. Depth counts nested conditions required to reach the innermost branch.

![Total runtime](filtering-runtime.png)

![Planning runtime](filtering-planning.png)

![Completed work](filtering-completed.png)

![Phase costs](filtering-phases.png)

2 paired repeats per chart and method; execution ceiling 540.0 seconds per run.
Dark bands show mean ±1 sample SD; light bands show ±2 SD, describing variation across paired repeats. Method order is seeded and shuffled for each repeat.
Input count is the full Boolean domain (2^fields); interaction strength stays at two.
The small finite domains are fully enumerated before filtering.
Gate depth changes branch rarity, fan-in and equivalent-output regions.

The engine runs real Helm checks with no shared outcome cache. Each invocation creates its own render-hash cache.
OS and Helm executable caches can remain warm. Chart generation, CLI startup and dependency preparation are excluded.
Planning and analysis are included in total engine time. The execution ceiling does not cap planning.

`sample-random` retains 70% subject to its normal 128-case floor. `filter` uses topology depth two and failure expansion.
`filter-adaptive` adds its measured floors; unmatched charts keep ordinary filtering. All methods use the same traversal seed.
The chart's injected markers change topology but are not asserted as lint failures in this successful-render load test.
Failure expansion is enabled for both filter presets; workloads with actual failing properties may expand toward the full plan.

| Fields | Depth | Repeat | Method | Selected | Completed | Total s | Planning s | Complexity s | Execution s | Status |
| ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 6 | 1 | 0 | baseline | 64 | 64 | 2.507 | 0.019 | 0.000 | 2.481 | passed |
| 6 | 1 | 0 | sample-random | 64 | 64 | 2.397 | 0.021 | 0.000 | 2.370 | passed |
| 6 | 1 | 0 | filter-adaptive | 5 | 5 | 0.286 | 0.069 | 0.020 | 0.210 | passed |
| 6 | 1 | 0 | filter | 5 | 5 | 0.247 | 0.049 | 0.000 | 0.193 | passed |
| 6 | 1 | 1 | baseline | 64 | 64 | 2.467 | 0.018 | 0.000 | 2.444 | passed |
| 6 | 1 | 1 | sample-random | 64 | 64 | 2.556 | 0.021 | 0.000 | 2.529 | passed |
| 6 | 1 | 1 | filter | 5 | 5 | 0.267 | 0.046 | 0.000 | 0.215 | passed |
| 6 | 1 | 1 | filter-adaptive | 5 | 5 | 0.293 | 0.067 | 0.017 | 0.221 | passed |
| 6 | 3 | 0 | baseline | 64 | 64 | 2.510 | 0.018 | 0.000 | 2.488 | passed |
| 6 | 3 | 0 | filter | 17 | 17 | 0.661 | 0.045 | 0.000 | 0.611 | passed |
| 6 | 3 | 0 | filter-adaptive | 17 | 17 | 0.832 | 0.090 | 0.043 | 0.735 | passed |
| 6 | 3 | 0 | sample-random | 64 | 64 | 2.490 | 0.020 | 0.000 | 2.465 | passed |
| 6 | 3 | 1 | filter-adaptive | 17 | 17 | 0.761 | 0.103 | 0.043 | 0.651 | passed |
| 6 | 3 | 1 | baseline | 64 | 64 | 2.469 | 0.020 | 0.000 | 2.443 | passed |
| 6 | 3 | 1 | sample-random | 64 | 64 | 2.774 | 0.018 | 0.000 | 2.751 | passed |
| 6 | 3 | 1 | filter | 17 | 17 | 0.811 | 0.066 | 0.000 | 0.739 | passed |
| 6 | 5 | 0 | filter | 29 | 29 | 1.231 | 0.060 | 0.000 | 1.165 | passed |
| 6 | 5 | 0 | sample-random | 64 | 64 | 2.527 | 0.020 | 0.000 | 2.500 | passed |
| 6 | 5 | 0 | filter-adaptive | 29 | 29 | 1.364 | 0.131 | 0.074 | 1.226 | passed |
| 6 | 5 | 0 | baseline | 64 | 64 | 2.433 | 0.023 | 0.000 | 2.404 | passed |
| 6 | 5 | 1 | filter | 29 | 29 | 1.152 | 0.057 | 0.000 | 1.090 | passed |
| 6 | 5 | 1 | filter-adaptive | 29 | 29 | 1.225 | 0.132 | 0.071 | 1.087 | passed |
| 6 | 5 | 1 | sample-random | 64 | 64 | 2.403 | 0.018 | 0.000 | 2.381 | passed |
| 6 | 5 | 1 | baseline | 64 | 64 | 2.375 | 0.023 | 0.000 | 2.347 | passed |
| 7 | 1 | 0 | filter | 9 | 9 | 0.419 | 0.093 | 0.000 | 0.321 | passed |
| 7 | 1 | 0 | filter-adaptive | 7 | 7 | 0.364 | 0.111 | 0.019 | 0.247 | passed |
| 7 | 1 | 0 | sample-random | 128 | 128 | 4.891 | 0.036 | 0.000 | 4.850 | passed |
| 7 | 1 | 0 | baseline | 128 | 128 | 5.066 | 0.039 | 0.000 | 5.022 | passed |
| 7 | 1 | 1 | filter-adaptive | 7 | 7 | 0.389 | 0.113 | 0.019 | 0.270 | passed |
| 7 | 1 | 1 | sample-random | 128 | 128 | 4.787 | 0.035 | 0.000 | 4.747 | passed |
| 7 | 1 | 1 | filter | 9 | 9 | 0.478 | 0.128 | 0.000 | 0.340 | passed |
| 7 | 1 | 1 | baseline | 128 | 128 | 4.843 | 0.041 | 0.000 | 4.796 | passed |
| 7 | 3 | 0 | filter-adaptive | 20 | 20 | 0.959 | 0.174 | 0.070 | 0.781 | passed |
| 7 | 3 | 0 | filter | 21 | 21 | 0.985 | 0.095 | 0.000 | 0.883 | passed |
| 7 | 3 | 0 | baseline | 128 | 128 | 4.929 | 0.039 | 0.000 | 4.885 | passed |
| 7 | 3 | 0 | sample-random | 128 | 128 | 4.879 | 0.039 | 0.000 | 4.835 | passed |
| 7 | 3 | 1 | baseline | 128 | 128 | 4.903 | 0.043 | 0.000 | 4.854 | passed |
| 7 | 3 | 1 | filter | 21 | 21 | 0.872 | 0.091 | 0.000 | 0.775 | passed |
| 7 | 3 | 1 | filter-adaptive | 20 | 20 | 0.969 | 0.201 | 0.098 | 0.762 | passed |
| 7 | 3 | 1 | sample-random | 128 | 128 | 5.015 | 0.040 | 0.000 | 4.968 | passed |
| 7 | 5 | 0 | filter-adaptive | 36 | 36 | 1.607 | 0.231 | 0.128 | 1.370 | passed |
| 7 | 5 | 0 | baseline | 128 | 128 | 5.058 | 0.038 | 0.000 | 5.015 | passed |
| 7 | 5 | 0 | filter | 37 | 37 | 1.531 | 0.109 | 0.000 | 1.416 | passed |
| 7 | 5 | 0 | sample-random | 128 | 128 | 4.890 | 0.042 | 0.000 | 4.842 | passed |
| 7 | 5 | 1 | sample-random | 128 | 128 | 4.943 | 0.042 | 0.000 | 4.895 | passed |
| 7 | 5 | 1 | filter | 37 | 37 | 1.483 | 0.086 | 0.000 | 1.391 | passed |
| 7 | 5 | 1 | filter-adaptive | 36 | 36 | 1.619 | 0.271 | 0.180 | 1.341 | passed |
| 7 | 5 | 1 | baseline | 128 | 128 | 4.724 | 0.041 | 0.000 | 4.677 | passed |
| 8 | 1 | 0 | sample-random | 180 | 180 | 6.939 | 0.088 | 0.000 | 6.844 | passed |
| 8 | 1 | 0 | filter-adaptive | 13 | 13 | 0.709 | 0.210 | 0.024 | 0.493 | passed |
| 8 | 1 | 0 | filter | 17 | 17 | 0.892 | 0.204 | 0.000 | 0.682 | passed |
| 8 | 1 | 0 | baseline | 256 | 256 | 9.628 | 0.100 | 0.000 | 9.521 | passed |
| 8 | 1 | 1 | sample-random | 180 | 180 | 6.874 | 0.103 | 0.000 | 6.765 | passed |
| 8 | 1 | 1 | filter | 17 | 17 | 0.827 | 0.197 | 0.000 | 0.624 | passed |
| 8 | 1 | 1 | baseline | 256 | 256 | 10.336 | 0.074 | 0.000 | 10.255 | passed |
| 8 | 1 | 1 | filter-adaptive | 13 | 13 | 0.694 | 0.200 | 0.025 | 0.488 | passed |
| 8 | 3 | 0 | baseline | 256 | 256 | 9.784 | 0.086 | 0.000 | 9.692 | passed |
| 8 | 3 | 0 | filter-adaptive | 34 | 34 | 1.631 | 0.345 | 0.119 | 1.279 | passed |
| 8 | 3 | 0 | sample-random | 180 | 180 | 6.855 | 0.079 | 0.000 | 6.768 | passed |
| 8 | 3 | 0 | filter | 35 | 35 | 1.759 | 0.204 | 0.000 | 1.546 | passed |
| 8 | 3 | 1 | filter | 35 | 35 | 1.544 | 0.200 | 0.000 | 1.337 | passed |
| 8 | 3 | 1 | filter-adaptive | 34 | 34 | 1.681 | 0.288 | 0.090 | 1.386 | passed |
| 8 | 3 | 1 | sample-random | 180 | 180 | 7.063 | 0.082 | 0.000 | 6.975 | passed |
| 8 | 3 | 1 | baseline | 256 | 256 | 9.899 | 0.084 | 0.000 | 9.809 | passed |
| 8 | 5 | 0 | sample-random | 180 | 180 | 6.956 | 0.113 | 0.000 | 6.836 | passed |
| 8 | 5 | 0 | filter | 58 | 58 | 2.405 | 0.208 | 0.000 | 2.188 | passed |
| 8 | 5 | 0 | baseline | 256 | 256 | 9.953 | 0.091 | 0.000 | 9.856 | passed |
| 8 | 5 | 0 | filter-adaptive | 58 | 58 | 2.767 | 0.512 | 0.306 | 2.248 | passed |
| 8 | 5 | 1 | filter-adaptive | 58 | 58 | 2.658 | 0.462 | 0.263 | 2.189 | passed |
| 8 | 5 | 1 | sample-random | 180 | 180 | 6.841 | 0.081 | 0.000 | 6.755 | passed |
| 8 | 5 | 1 | filter | 58 | 58 | 2.413 | 0.200 | 0.000 | 2.206 | passed |
| 8 | 5 | 1 | baseline | 256 | 256 | 9.823 | 0.088 | 0.000 | 9.729 | passed |
| 9 | 1 | 0 | baseline | 512 | 512 | 19.966 | 0.188 | 0.000 | 19.771 | passed |
| 9 | 1 | 0 | filter | 33 | 33 | 1.727 | 0.386 | 0.000 | 1.333 | passed |
| 9 | 1 | 0 | sample-random | 359 | 359 | 14.215 | 0.173 | 0.000 | 14.035 | passed |
| 9 | 1 | 0 | filter-adaptive | 33 | 33 | 1.679 | 0.405 | 0.026 | 1.267 | passed |
| 9 | 1 | 1 | baseline | 512 | 512 | 19.753 | 0.175 | 0.000 | 19.571 | passed |
| 9 | 1 | 1 | sample-random | 359 | 359 | 13.889 | 0.177 | 0.000 | 13.704 | passed |
| 9 | 1 | 1 | filter | 33 | 33 | 1.691 | 0.340 | 0.000 | 1.345 | passed |
| 9 | 1 | 1 | filter-adaptive | 33 | 33 | 1.672 | 0.402 | 0.026 | 1.262 | passed |
| 9 | 3 | 0 | sample-random | 359 | 359 | 13.875 | 0.171 | 0.000 | 13.698 | passed |
| 9 | 3 | 0 | filter | 75 | 75 | 3.388 | 0.392 | 0.000 | 2.989 | passed |
| 9 | 3 | 0 | baseline | 512 | 512 | 19.557 | 0.169 | 0.000 | 19.381 | passed |
| 9 | 3 | 0 | filter-adaptive | 75 | 75 | 3.545 | 0.697 | 0.293 | 2.840 | passed |
| 9 | 3 | 1 | baseline | 512 | 512 | 19.526 | 0.176 | 0.000 | 19.344 | passed |
| 9 | 3 | 1 | filter | 75 | 75 | 3.206 | 0.428 | 0.000 | 2.771 | passed |
| 9 | 3 | 1 | filter-adaptive | 75 | 75 | 3.563 | 0.654 | 0.267 | 2.902 | passed |
| 9 | 3 | 1 | sample-random | 359 | 359 | 14.281 | 0.163 | 0.000 | 14.113 | passed |
| 9 | 5 | 0 | filter | 127 | 127 | 5.183 | 0.445 | 0.000 | 4.731 | passed |
| 9 | 5 | 0 | sample-random | 359 | 359 | 16.251 | 0.164 | 0.000 | 16.080 | passed |
| 9 | 5 | 0 | baseline | 512 | 512 | 26.110 | 0.276 | 0.000 | 25.825 | passed |
| 9 | 5 | 0 | filter-adaptive | 127 | 127 | 6.343 | 1.286 | 0.629 | 5.050 | passed |
| 9 | 5 | 1 | filter-adaptive | 127 | 127 | 6.624 | 1.294 | 0.697 | 5.324 | passed |
| 9 | 5 | 1 | baseline | 512 | 512 | 20.847 | 0.195 | 0.000 | 20.645 | passed |
| 9 | 5 | 1 | sample-random | 359 | 359 | 14.500 | 0.173 | 0.000 | 14.319 | passed |
| 9 | 5 | 1 | filter | 127 | 127 | 5.811 | 0.473 | 0.000 | 5.331 | passed |

Raw timings and fallback decisions (local run data) · Full measurements (local run data) · Chart recipes (local run data)
