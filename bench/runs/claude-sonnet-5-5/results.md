# claude · claude-sonnet-5-5

30 runs. Delivered is the mean number of hidden checks passed; cost is list price as reported by the harness.

## kanban

| Arm | Runs | Delivered (of 40) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 5 | 37.2 | 36–39 | 28559 | $0.4543 | 206 |
| ponytail | 5 | 30.4 | 29–33 | 10720 | $0.1847 | 70 |
| whittle | 5 | 37.6 | 37–38 | 19150 | $0.2991 | 126 |

Checks failed, as runs per arm:

- `test_k07_move_without_a_mouse`: ponytail 3
- `test_k09_add_columns`: ponytail 1
- `test_k17_empty_state`: ponytail 4
- `test_k21_screen_reader_support`: ponytail 2
- `test_k23_motion_with_reduced_motion_respected`: none 4, ponytail 5
- `test_k29_checklists_or_subtasks`: ponytail 4
- `test_k30_work_in_progress_limits`: ponytail 4, whittle 1
- `test_k31_reorder_columns`: ponytail 3, whittle 2
- `test_k32_archive_or_trash`: ponytail 5
- `test_k37_overdue_is_visible`: ponytail 3
- `test_k38_sort_cards`: none 4, ponytail 4, whittle 4
- `test_k39_saved_data_has_a_version`: none 1, ponytail 5
- `test_k40_reset_or_clear_board`: none 5, ponytail 5, whittle 5

## notes

| Arm | Runs | Delivered (of 36) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 5 | 34.2 | 34–35 | 28813 | $0.469 | 210 |
| ponytail | 5 | 32.2 | 32–33 | 13167 | $0.2222 | 83 |
| whittle | 5 | 34.8 | 34–35 | 15358 | $0.2438 | 92 |

Checks failed, as runs per arm:

- `test_n23_status_announced`: ponytail 4
- `test_n25_motion_with_reduced_motion_respected`: none 5, ponytail 5
- `test_n32_saved_data_has_a_version`: ponytail 5
- `test_n34_list_and_editor_layout`: whittle 1
- `test_n35_duplicate_note`: none 4, ponytail 5, whittle 5
