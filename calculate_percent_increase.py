def percent_increase(start, final):
    return (final - start) / start


k1_human_weighted_sum_top_k_hits = [0.25892857142857145, 0.30357142857142855, 0.3482142857142857, 0.33035714285714285, 0.375, 0.38392857142857145, 0.38392857142857145, 0.3482142857142857, 0.35714285714285715, 0.3392857142857143, 0.2857142857142857]
k1_machine_weighted_sum_top_k_hits = [0.21428571428571427, 0.24107142857142858, 0.25, 0.22321428571428573, 0.23214285714285715, 0.25892857142857145, 0.2767857142857143, 0.25, 0.25892857142857145, 0.25, 0.22321428571428573]

print('K = 1')
# print(k1_human_weighted_sum_top_k_hits[0], k1_human_weighted_sum_top_k_hits[-1], k1_human_weighted_sum_top_k_hits[5])
print(f'Percent increase from text-only to image-weight=0.6: {percent_increase(k1_human_weighted_sum_top_k_hits[0], k1_human_weighted_sum_top_k_hits[5]):.0%}')
print(f'Percent increase from sketch-only to image-weight=0.6: {percent_increase(k1_human_weighted_sum_top_k_hits[-1], k1_human_weighted_sum_top_k_hits[5]):.0%}')


k5_human_weighted_sum_top_k_hits = [0.4375, 0.5089285714285714, 0.5446428571428571, 0.5714285714285714, 0.5803571428571429, 0.6071428571428571, 0.6339285714285714, 0.6517857142857143, 0.625, 0.5982142857142857, 0.5357142857142857]
k5_machine_weighted_sum_top_k_hits = [0.42857142857142855, 0.45535714285714285, 0.4375, 0.44642857142857145, 0.49107142857142855, 0.5089285714285714, 0.4732142857142857, 0.4642857142857143, 0.4375, 0.42857142857142855, 0.4107142857142857]

print('K = 5')
# print(k5_human_weighted_sum_top_k_hits[0], k5_human_weighted_sum_top_k_hits[-1], k5_human_weighted_sum_top_k_hits[5])
print(f'Percent increase from text-only to image-weight=0.6: {percent_increase(k5_human_weighted_sum_top_k_hits[0], k5_human_weighted_sum_top_k_hits[5]):.0%}')
print(f'Percent increase from sketch-only to image-weight=0.6: {percent_increase(k5_human_weighted_sum_top_k_hits[-1], k5_human_weighted_sum_top_k_hits[5]):.0%}')


k10_human_weighted_sum_top_k_hits = [0.5714285714285714, 0.625, 0.6339285714285714, 0.6607142857142857, 0.6875, 0.6875, 0.7410714285714286, 0.7053571428571429, 0.6785714285714286, 0.6696428571428571, 0.625]
k10_machine_weighted_sum_top_k_hits = [0.5446428571428571, 0.5714285714285714, 0.5714285714285714, 0.5535714285714286, 0.5982142857142857, 0.5982142857142857, 0.6071428571428571, 0.5535714285714286, 0.5625, 0.5, 0.45535714285714285]

print('K = 10')
# print(k10_human_weighted_sum_top_k_hits[0], k10_human_weighted_sum_top_k_hits[-1], k10_human_weighted_sum_top_k_hits[5])
print(f'Percent increase from text-only to image-weight=0.6: {percent_increase(k10_human_weighted_sum_top_k_hits[0], k10_human_weighted_sum_top_k_hits[5]):.0%}')
print(f'Percent increase from sketch-only to image-weight=0.6: {percent_increase(k10_human_weighted_sum_top_k_hits[-1], k10_human_weighted_sum_top_k_hits[5]):.0%}')
