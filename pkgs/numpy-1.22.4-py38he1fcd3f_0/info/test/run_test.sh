

set -ex



f2py -h
python -c "import numpy, sys; sys.exit(not numpy.test(verbose=1, label='full', tests=None, extra_argv=['-k', 'not (_not_a_real_test or Test_ARM_Features or test_new_policy or test_partial_iteration_cleanup)', '-nauto', '--timeout=3000', '--durations=50']))"
exit 0
