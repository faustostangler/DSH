import assets.helper as b3

def my_periodic_task():
    # value = 'update_b3_companies'
    # value = b3.update_b3_companies(value)

    # value = 'world_markets'
    # value = b3.update_world_markets(value)

    # value = 'yahoo_cotahist'
    # value = b3.yahoo_cotahist(value)

    # value = 'nsd'
    # value = b3.get_nsd_links(value)

    value = 'nsd'
    value = b3.get_dre(value)

    print("All updated!")

if __name__ == "__main__":
    my_periodic_task()  