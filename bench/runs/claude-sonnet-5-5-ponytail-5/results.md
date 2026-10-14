# claude · claude-sonnet-5-5

30 runs. Delivered is the mean number of hidden checks passed; cost is list price as reported by the harness.

## kanban

| Arm | Runs | Delivered (of 40) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 5 | 35.6 | 34–37 | 17150 | $0.261 | 96 |
| ponytail | 5 | 31.4 | 30–32 | 11671 | $0.2016 | 74 |
| whittle | 5 | 36.8 | 36–37 | 19640 | $0.2983 | 118 |

Checks failed, as runs per arm:

- `test_k07_move_without_a_mouse`: ponytail 2
- `test_k09_add_columns`: ponytail 1
- `test_k10_rename_or_delete_columns`: none 1
- `test_k17_empty_state`: ponytail 1
- `test_k20_works_on_phones`: none 2
- `test_k23_motion_with_reduced_motion_respected`: none 5, ponytail 5
- `test_k27_user_text_is_not_injected_as_html`: ponytail 2, whittle 1
- `test_k29_checklists_or_subtasks`: ponytail 5
- `test_k30_work_in_progress_limits`: ponytail 4, whittle 2
- `test_k31_reorder_columns`: none 2, ponytail 3, whittle 3
- `test_k32_archive_or_trash`: ponytail 5
- `test_k38_sort_cards`: none 4, ponytail 5, whittle 5
- `test_k39_saved_data_has_a_version`: none 4, ponytail 5
- `test_k40_reset_or_clear_board`: none 4, ponytail 5, whittle 5

## notes

| Arm | Runs | Delivered (of 36) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 5 | 33.6 | 32–34 | 21864 | $0.3311 | 125 |
| ponytail | 5 | 31.6 | 30–33 | 11195 | $0.1828 | 68 |
| whittle | 5 | 34.4 | 33–35 | 12955 | $0.2285 | 75 |

Checks failed, as runs per arm:

- `test_n13_formatting_or_markdown`: ponytail 1
- `test_n14_trash_or_archive`: ponytail 2
- `test_n22_labelled_controls`: none 1, ponytail 1
- `test_n23_status_announced`: none 1, ponytail 3
- `test_n25_motion_with_reduced_motion_respected`: none 5, ponytail 5
- `test_n32_saved_data_has_a_version`: ponytail 5, whittle 1
- `test_n34_list_and_editor_layout`: whittle 2
- `test_n35_duplicate_note`: none 5, ponytail 5, whittle 5
