# fruit_shop/tasks.py
import time
def order_fruit(fruit, num_fruit):
	time.sleep(num_fruit)   # e.g. 2 apples take 2 secs
	return '%s_%s' % (fruit, num_fruit)
