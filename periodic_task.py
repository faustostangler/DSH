import assets.helper as b3

def my_periodic_task():
    value = b3.update_b3_companies(value)
    print("All updated!")

if __name__ == "__main__":
    my_periodic_task()