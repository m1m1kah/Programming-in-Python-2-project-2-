import pytest
from PriceTracker import PriceTracker
from datetime import datetime, timedelta
import random

def check_window(data, start, end):
    for (time, dp) in data:
        p = dp[0]
        minp = dp[1]
        if start <= time <= end:
            true_min = min([dp[0] for (t, dp) in data if t >= time - timedelta(days=10) and t <= time])
            assert minp == true_min

def make_constant_prices(num, avg_gap):
    random.seed(10)
    cur = datetime(2025, 4, 1)
    data = []
    for i in range(num):
        td = timedelta(hours=random.uniform(0,2*avg_gap))
        cur += td
        data.append((cur, 1.0))
    cur = datetime(2025, 4, 15)
    for i in range(num):
        td = timedelta(hours=random.uniform(0,1))
        cur += td
        data.append((cur, 1.0))
    return data
constant_prices = make_constant_prices(300,1)

def make_random_prices(num, avg_gap):
    random.seed(10)
    cur = datetime(2025, 4, 1)
    data = []
    for i in range(num):
        td = timedelta(hours=random.uniform(0,2*avg_gap))
        cur += td
        data.append((cur, random.uniform(3,10)))
    return data
random_prices_1 = make_random_prices(60,12)
random_prices_2 = make_random_prices(1000,1)
random_prices_3 = make_random_prices(100000,0.05)

def make_increasing_prices(avg_gap, num):
    random.seed(10)
    cur = datetime(2025, 4, 1)
    cur_price = 0.1
    data = []
    for i in range(num):
        td = timedelta(hours=random.uniform(0,2*avg_gap))
        cur += td
        cur_price *= random.uniform(1,1.5)
        data.append((cur, cur_price))
    return data
increasing_prices_1 = make_increasing_prices(60, 12)
increasing_prices_2 = make_increasing_prices(1000, 1)

def make_decreasing_prices(avg_gap, num):
    random.seed(10)
    cur = datetime(2025, 4, 1)
    cur_price = 1000
    data = []
    for i in range(num):
        td = timedelta(hours=random.uniform(0,2*avg_gap))
        cur += td
        cur_price *= random.uniform(0.9, 1.0)
        data.append((cur, cur_price))
    return data
decreasing_prices_1 = make_decreasing_prices(60,12)
decreasing_prices_2 = make_decreasing_prices(1000,1)

def test_empty():
    pt = PriceTracker()
    start = datetime(2025, 4, 1)
    end = datetime(2025, 4, 30)
    data = pt.get_price_data(start, end)
    assert data == []

def test_single():
    pt = PriceTracker()
    start = datetime(2025, 4, 1)
    end = datetime(2025, 4, 30)
    pt.add_price(start, 1.0)
    data = pt.get_price_data(start, end)
    assert len(data) == 1
    (t, dp) = data[0]
    assert t == start
    assert dp[0] == 1.0
    assert dp[1] == 1.0

def test_range_1():
    pt = PriceTracker()
    ts = [datetime(2025, 4, i, i) for i in range(1,20)]
    pt = PriceTracker()
    for t in ts:
        pt.add_price(t, 1.0)
    start = datetime(2025, 4, 1)
    end = datetime(2025, 4, 10)
    results = [(t, (1.0, 1.0)) for t in ts if start <= t and t <= end]
    data = pt.get_price_data(start, end)
    assert [(time, (dp[0], dp[1])) for (time, dp) in data] == results

def test_range_2():
    pt = PriceTracker()
    ts = [datetime(2025, 4, i, i) for i in range(1,20)]
    pt = PriceTracker()
    for t in ts:
        pt.add_price(t, 1.0)
    start = datetime(2025, 4, 3)
    end = datetime(2025, 4, 9)
    results = [(t, (1.0, 1.0)) for t in ts if start <= t and t <= end]
    data = pt.get_price_data(start, end)
    assert [(time, (dp[0], dp[1])) for (time, dp) in data] == results

@pytest.mark.parametrize("prices", [increasing_prices_1, 
                                    increasing_prices_2,
                                    decreasing_prices_1,
                                    decreasing_prices_2,
                                    constant_prices,
                                    random_prices_1,
                                    random_prices_2
                                    ])
def test_window(prices):
    pt = PriceTracker()
    for d in prices:
        pt.add_price(*d)
    start = prices[0][0]
    end = prices[-1][0]
    data = pt.get_price_data(start, end)
    print(data)
    check_window(data,start,end)

@pytest.mark.timeout(120)
def test_efficiency():
    pt = PriceTracker()
    for d in random_prices_3:
        pt.add_price(*d)
    assert True
    
