import numpy as np

def verify():
    # Function f(t) from the condition PQ = QR
    def f(t):
        return 2 * np.log(6 * t / (np.exp(3 * t) - 1))
    
    # Test with small positive values of t
    test_values = [0.001, 0.0001, 0.00001]
    
    for t_val in test_values:
        k = f(t_val)
        
        # Point coordinates
        P_y = np.exp(k / 2)
        Q_y = np.exp(k / 2 + 3 * t_val)
        R_x = k + 6 * t_val
        
        # Distance PQ (vertical distance at x=k)
        PQ_dist = Q_y - P_y
        
        # Distance QR (horizontal distance at y=e^(k/2+3t))
        QR_dist = 6 * t_val
        
        # Verify the condition PQ = QR
        if np.abs(PQ_dist - QR_dist) > 1e-8:
            print('VERIFY_FAIL')
            return
    
    # Check the limit as t -> 0+
    # Expected: ln(4)
    expected_limit = np.log(4)
    computed_limit = f(0.000001)  # Very small t approaches the limit
    
    # The limit should approach ln(4) ≈ 1.38629
    if np.abs(computed_limit - expected_limit) > 1e-3:
        print('VERIFY_FAIL')
        return
    
    print('VERIFY_PASS')

verify()