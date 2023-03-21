import assets.helper as b3

def my_periodic_task():
    # value = 'update_b3_companies'
    # value = b3.update_b3_companies(value)

    value = 'world_markets'
    value = b3.update_world_markets(value)

    print("All updated!")

if __name__ == "__main__":
    my_periodic_task()