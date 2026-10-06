# pi · openai-codex/gpt-6-luna

220 runs. Delivered is the mean number of hidden checks passed; cost is list price as reported by the harness.

## expense-report

| Arm | Runs | Delivered (of 32) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 10 | 31.5 | 30–32 | 2464 | $0.0027 | 64 |
| terse | 10 | 30.9 | 30–32 | 2635 | $0.0026 | 80 |
| ponytail | 10 | 30.5 | 29–32 | 2369 | $0.0026 | 63 |
| caveman | 10 | 30.5 | 30–31 | 2557 | $0.0029 | 74 |
| whittle | 10 | 30.7 | 29–32 | 2470 | $0.0024 | 63 |

Checks failed, as runs per arm:

- `test_r12_by_category_columns_and_order`: terse 2
- `test_r17_json_groups`: ponytail 1, terse 1, whittle 1
- `test_r21_currency_symbol_only_in_table`: ponytail 1, whittle 1
- `test_r23_invalid_date`: caveman 6, none 2, ponytail 4, terse 2, whittle 2
- `test_r27_top_n_largest_first`: ponytail 2, whittle 1
- `test_r28_refunds_in_parentheses_still_subtract`: terse 1
- `test_r30_group_names_title_cased_in_table_only`: caveman 6, none 2, ponytail 6, terse 4, whittle 7
- `test_r31_help_lists_every_flag_and_an_example`: caveman 3, none 1, ponytail 1, terse 1, whittle 1

## kanban

| Arm | Runs | Delivered (of 40) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 10 | 27.6 | 26–30 | 8007 | $0.0058 | 159 |
| ponytail | 10 | 26.3 | 24–28 | 6317 | $0.0051 | 128 |
| caveman | 10 | 27 | 24–29 | 7955 | $0.0059 | 161 |
| whittle | 10 | 31.2 | 30–33 | 6114 | $0.0046 | 124 |

Checks failed, as runs per arm:

- `test_k01_opens_without_network_or_build`: caveman 5, none 7, ponytail 5, whittle 4
- `test_k02_three_default_columns`: caveman 1, none 1, ponytail 1
- `test_k07_move_without_a_mouse`: caveman 7, none 8, ponytail 9, whittle 7
- `test_k09_add_columns`: caveman 9, none 7, ponytail 10, whittle 9
- `test_k10_rename_or_delete_columns`: caveman 10, none 9, ponytail 9, whittle 8
- `test_k15_export_or_import`: none 1
- `test_k16_undo_or_confirmation_before_losing_work`: caveman 3, none 1
- `test_k19_dark_mode`: caveman 8, none 8, ponytail 8, whittle 1
- `test_k21_screen_reader_support`: caveman 2, ponytail 1
- `test_k22_visible_focus`: none 1, ponytail 1, whittle 1
- `test_k23_motion_with_reduced_motion_respected`: caveman 10, none 10, ponytail 10
- `test_k24_keyboard_shortcuts_or_help`: none 1, ponytail 1
- `test_k28_more_than_a_single_script_blob`: caveman 4, none 2, ponytail 3, whittle 6
- `test_k29_checklists_or_subtasks`: caveman 9, none 8, ponytail 10, whittle 9
- `test_k30_work_in_progress_limits`: caveman 10, none 10, ponytail 10, whittle 9
- `test_k31_reorder_columns`: caveman 5, none 7, ponytail 9, whittle 3
- `test_k32_archive_or_trash`: caveman 10, none 10, ponytail 10, whittle 9
- `test_k33_undo`: caveman 10, none 9, ponytail 10
- `test_k34_tabs_stay_in_sync`: caveman 10, none 10, ponytail 10, whittle 9
- `test_k37_overdue_is_visible`: ponytail 1
- `test_k38_sort_cards`: caveman 10, none 8, ponytail 10, whittle 10
- `test_k39_saved_data_has_a_version`: caveman 6, none 6, ponytail 8, whittle 1
- `test_k40_reset_or_clear_board`: caveman 1, ponytail 1, whittle 2

## pricing-page

| Arm | Runs | Delivered (of 26) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 10 | 23.9 | 23–25 | 4735 | $0.0036 | 97 |
| ponytail | 10 | 24.2 | 22–25 | 4124 | $0.0033 | 85 |
| caveman | 10 | 23.9 | 23–25 | 4328 | $0.0034 | 90 |
| whittle | 10 | 24.1 | 23–25 | 4694 | $0.0034 | 98 |

Checks failed, as runs per arm:

- `test_b04_three_plans_as_headings`: none 1, ponytail 2
- `test_b05_monthly_prices`: caveman 1, none 1, ponytail 1, whittle 1
- `test_b07_billing_switch_is_a_real_control`: caveman 5, none 2, whittle 3
- `test_b09_price_change_is_announced`: caveman 9, none 9, ponytail 7, whittle 7
- `test_b14_table_is_readable_by_screen_readers`: caveman 6, none 8, ponytail 7, whittle 8
- `test_b23_visible_keyboard_focus`: ponytail 1

## report-over-time

| Arm | Runs | Delivered (of 40) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 10 | 38.5 | 38–40 | 5842 | $0.0081 | 179 |
| ponytail | 10 | 38.9 | 37–40 | 5517 | $0.008 | 163 |
| caveman | 10 | 38.6 | 38–40 | 6093 | $0.0081 | 183 |
| whittle | 10 | 38.7 | 37–40 | 5964 | $0.0077 | 180 |

Checks failed, as runs per arm:

- `test_r17_json_groups`: whittle 1
- `test_r22_missing_file`: ponytail 1
- `test_r23_invalid_date`: caveman 2, none 6, ponytail 3, whittle 3
- `test_r24_from_after_to`: none 1, ponytail 1
- `test_r27_top_n_largest_first`: none 1, whittle 1
- `test_r28_refunds_in_parentheses_still_subtract`: caveman 1
- `test_r30_group_names_title_cased_in_table_only`: caveman 8, none 5, ponytail 3, whittle 5
- `test_r31_help_lists_every_flag_and_an_example`: caveman 3, none 2, ponytail 3, whittle 2
- `test_r39_markdown_total_row`: whittle 1

## status-page

| Arm | Runs | Delivered (of 36) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 10 | 35.7 | 35–36 | 2215 | $0.0023 | 62 |
| terse | 10 | 35.6 | 35–36 | 2243 | $0.0025 | 57 |
| ponytail | 10 | 35.5 | 35–36 | 2014 | $0.0025 | 57 |
| caveman | 10 | 35.8 | 35–36 | 2216 | $0.0024 | 57 |
| whittle | 10 | 35.6 | 35–36 | 2217 | $0.0021 | 54 |

Checks failed, as runs per arm:

- `test_r11_banner_singular`: caveman 2, none 3, ponytail 5, terse 4, whittle 4
