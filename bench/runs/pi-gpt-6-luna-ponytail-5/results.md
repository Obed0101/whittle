# pi · openai-codex/gpt-6-luna

220 runs. Delivered is the mean number of hidden checks passed; cost is list price as reported by the harness.

## expense-report

| Arm | Runs | Delivered (of 32) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 10 | 30.9 | 30–32 | 2508 | $0.0026 | 28 |
| terse | 10 | 29.5 | 16–32 | 2546 | $0.0025 | 30 |
| ponytail | 10 | 30.7 | 30–32 | 2350 | $0.0024 | 28 |
| caveman | 10 | 30.7 | 29–32 | 2636 | $0.0026 | 32 |
| whittle | 10 | 27.5 | 0–32 | 2528 | $0.0025 | 30 |

Checks failed, as runs per arm:

- `test_r01_table_header_columns_in_order`: terse 1, whittle 1
- `test_r02_dashes_under_header`: terse 1, whittle 1
- `test_r03_sorted_by_date_keeping_file_order_on_ties`: terse 1, whittle 1
- `test_r04_amounts_two_decimals_thousands_right_aligned`: terse 1, whittle 1
- `test_r05_long_note_cut_to_23_chars_and_ellipsis`: terse 1, whittle 1
- `test_r06_total_line`: terse 1, whittle 1
- `test_r07_nothing_to_show`: whittle 1
- `test_r08_category_filter_ignores_case_and_repeats`: terse 1, whittle 1
- `test_r09_from_is_inclusive`: terse 1, whittle 1
- `test_r10_to_is_inclusive`: terse 1, whittle 1
- `test_r11_min_amount_is_inclusive`: terse 1, whittle 1
- `test_r12_by_category_columns_and_order`: whittle 1
- `test_r13_by_month_oldest_first`: whittle 2
- `test_r14_grouped_output_ends_with_total`: whittle 2
- `test_r15_grouped_count_column`: whittle 2
- `test_r16_json_rows`: whittle 1
- `test_r17_json_groups`: whittle 1
- `test_r18_json_two_space_indent_and_final_newline`: whittle 1
- `test_r19_csv_format`: whittle 1
- `test_r20_notes_not_cut_outside_the_table`: whittle 1
- `test_r21_currency_symbol_only_in_table`: terse 1, whittle 1
- `test_r22_missing_file`: whittle 1
- `test_r23_invalid_date`: caveman 4, none 5, ponytail 4, terse 2, whittle 3
- `test_r24_from_after_to`: whittle 1
- `test_r25_unknown_format_exits_2`: whittle 1
- `test_r26_invalid_amount_rows_skipped_with_plural_warning`: terse 1, whittle 1
- `test_r27_top_n_largest_first`: caveman 1, none 1, ponytail 1, terse 1, whittle 1
- `test_r28_refunds_in_parentheses_still_subtract`: terse 1, whittle 1
- `test_r29_no_header`: terse 1, whittle 1
- `test_r30_group_names_title_cased_in_table_only`: caveman 4, none 4, ponytail 7, terse 7, whittle 6
- `test_r31_help_lists_every_flag_and_an_example`: caveman 4, none 1, ponytail 1, terse 1, whittle 4
- `test_r32_runs_as_a_module`: whittle 1

## kanban

| Arm | Runs | Delivered (of 40) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 10 | 27.2 | 25–30 | 7476 | $0.0053 | 59 |
| ponytail | 10 | 26.7 | 24–28 | 6283 | $0.0049 | 54 |
| caveman | 10 | 28.1 | 27–30 | 8617 | $0.0066 | 71 |
| whittle | 10 | 30 | 27–35 | 5777 | $0.0042 | 46 |

Checks failed, as runs per arm:

- `test_k01_opens_without_network_or_build`: caveman 7, none 8, ponytail 5, whittle 4
- `test_k02_three_default_columns`: ponytail 1, whittle 1
- `test_k07_move_without_a_mouse`: caveman 7, none 7, ponytail 9, whittle 8
- `test_k09_add_columns`: caveman 9, none 10, ponytail 10, whittle 9
- `test_k10_rename_or_delete_columns`: caveman 9, none 10, ponytail 10, whittle 8
- `test_k17_empty_state`: none 1
- `test_k19_dark_mode`: caveman 8, none 9, ponytail 10, whittle 2
- `test_k21_screen_reader_support`: ponytail 1
- `test_k22_visible_focus`: ponytail 1, whittle 2
- `test_k23_motion_with_reduced_motion_respected`: caveman 10, none 8, ponytail 9, whittle 1
- `test_k24_keyboard_shortcuts_or_help`: ponytail 3, whittle 2
- `test_k28_more_than_a_single_script_blob`: caveman 1, none 2, ponytail 2, whittle 6
- `test_k29_checklists_or_subtasks`: caveman 10, none 10, ponytail 10, whittle 10
- `test_k30_work_in_progress_limits`: caveman 10, none 10, ponytail 10, whittle 10
- `test_k31_reorder_columns`: caveman 6, none 5, ponytail 5, whittle 6
- `test_k32_archive_or_trash`: caveman 8, none 9, ponytail 10, whittle 8
- `test_k33_undo`: caveman 10, none 10, ponytail 10, whittle 1
- `test_k34_tabs_stay_in_sync`: caveman 10, none 10, ponytail 10, whittle 10
- `test_k36_card_editor_dialog`: none 1
- `test_k37_overdue_is_visible`: whittle 1
- `test_k38_sort_cards`: caveman 8, none 10, ponytail 10, whittle 10
- `test_k39_saved_data_has_a_version`: caveman 6, none 7, ponytail 4
- `test_k40_reset_or_clear_board`: none 1, ponytail 3, whittle 1

## pricing-page

| Arm | Runs | Delivered (of 26) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 10 | 23.5 | 22–25 | 4372 | $0.0032 | 37 |
| ponytail | 10 | 24.6 | 24–26 | 4105 | $0.0031 | 36 |
| caveman | 10 | 24.4 | 23–25 | 4391 | $0.0032 | 38 |
| whittle | 10 | 23.6 | 23–24 | 4708 | $0.0036 | 45 |

Checks failed, as runs per arm:

- `test_b04_three_plans_as_headings`: caveman 1, none 2, whittle 1
- `test_b05_monthly_prices`: caveman 1, none 3
- `test_b07_billing_switch_is_a_real_control`: caveman 2, none 3, ponytail 2, whittle 8
- `test_b09_price_change_is_announced`: caveman 6, none 9, ponytail 6, whittle 9
- `test_b14_table_is_readable_by_screen_readers`: caveman 6, none 8, ponytail 6, whittle 6

## report-over-time

| Arm | Runs | Delivered (of 40) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 10 | 38.4 | 36–40 | 5902 | $0.0073 | 82 |
| ponytail | 10 | 38.6 | 36–40 | 5776 | $0.0074 | 92 |
| caveman | 10 | 38.6 | 37–40 | 6124 | $0.0071 | 89 |
| whittle | 10 | 36.5 | 19–40 | 6104 | $0.0079 | 84 |

Checks failed, as runs per arm:

- `test_r01_table_header_columns_in_order`: whittle 2
- `test_r02_dashes_under_header`: whittle 1
- `test_r03_sorted_by_date_keeping_file_order_on_ties`: whittle 1
- `test_r04_amounts_two_decimals_thousands_right_aligned`: ponytail 1, whittle 3
- `test_r05_long_note_cut_to_23_chars_and_ellipsis`: whittle 1
- `test_r06_total_line`: whittle 1
- `test_r08_category_filter_ignores_case_and_repeats`: whittle 1
- `test_r09_from_is_inclusive`: whittle 1
- `test_r10_to_is_inclusive`: whittle 1
- `test_r11_min_amount_is_inclusive`: whittle 1
- `test_r12_by_category_columns_and_order`: whittle 1
- `test_r13_by_month_oldest_first`: whittle 1
- `test_r16_json_rows`: whittle 1
- `test_r18_json_two_space_indent_and_final_newline`: whittle 1
- `test_r21_currency_symbol_only_in_table`: ponytail 1, whittle 1
- `test_r23_invalid_date`: caveman 3, none 1, ponytail 3, whittle 5
- `test_r26_invalid_amount_rows_skipped_with_plural_warning`: whittle 1
- `test_r27_top_n_largest_first`: none 2, ponytail 1, whittle 1
- `test_r28_refunds_in_parentheses_still_subtract`: whittle 1
- `test_r29_no_header`: ponytail 1, whittle 1
- `test_r30_group_names_title_cased_in_table_only`: caveman 7, none 6, ponytail 4, whittle 4
- `test_r31_help_lists_every_flag_and_an_example`: caveman 4, none 4, ponytail 2, whittle 1
- `test_r33_exclude_ignores_case`: whittle 1
- `test_r34_exclude_repeats`: whittle 1
- `test_r35_exclude_changes_the_total`: whittle 1
- `test_r37_markdown_header_and_alignment_row`: none 1
- `test_r38_markdown_rows`: none 1
- `test_r39_markdown_total_row`: none 1, ponytail 1

## status-page

| Arm | Runs | Delivered (of 36) | Range | Output tokens | Cost | Seconds |
|---|---|---|---|---|---|---|
| none | 10 | 35.6 | 35–36 | 2214 | $0.0021 | 24 |
| terse | 10 | 35.4 | 34–36 | 2084 | $0.0019 | 23 |
| ponytail | 10 | 35.9 | 35–36 | 2080 | $0.0021 | 24 |
| caveman | 10 | 35.4 | 35–36 | 2268 | $0.0025 | 26 |
| whittle | 10 | 35.4 | 34–36 | 2205 | $0.0022 | 24 |

Checks failed, as runs per arm:

- `test_r04_title_counts_operational`: terse 2, whittle 3
- `test_r11_banner_singular`: caveman 6, none 4, ponytail 1, terse 4, whittle 3
