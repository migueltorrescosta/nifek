def stakes_raw_queries(pk, key):
    """
    These queries return triplets "stake_id, owned_id, owner_id, stake" recursively from one asset
    """
    queries = {
        "all": f"""
            (
                WITH RECURSIVE recursive_assets(id, owned_id, owner_id, stake) AS (
                    SELECT id, owned_id, owner_id, stake
                    FROM hold_stake
                    WHERE owner_id = {pk}
                    UNION ALL
                    SELECT s.id, s.owned_id, s.owner_id, s.stake
                    FROM recursive_assets AS r, hold_stake AS s
                    WHERE r.owned_id = s.owner_id 
                    )
                SELECT * FROM recursive_assets
            )
            UNION
            (
                WITH RECURSIVE recursive_shareholders(id, owned_id, owner_id, stake) AS (
                    SELECT id, owned_id, owner_id, stake
                    FROM hold_stake
                    WHERE owned_id = {pk}
                    UNION ALL
                    SELECT s.id, s.owned_id, s.owner_id, s.stake
                    FROM recursive_shareholders AS r, hold_stake AS s
                    WHERE r.owner_id = s.owned_id 
                    )
                SELECT * FROM recursive_shareholders
            )
        """,
        "assets": f"""
        WITH RECURSIVE recursive_assets(id, owned_id, owner_id, stake) AS (
            SELECT id, owned_id, owner_id, stake
            FROM hold_stake
            WHERE owner_id = {pk}
            UNION ALL
            SELECT s.id, s.owned_id, s.owner_id, s.stake
            FROM recursive_assets AS r, hold_stake AS s
            WHERE r.owned_id = s.owner_id 
            )
        SELECT DISTINCT * FROM recursive_assets
    """,
        "shareholders": f"""
        WITH RECURSIVE recursive_shareholders(id, owned_id, owner_id, stake) AS (
            SELECT id, owned_id, owner_id, stake
            FROM hold_stake
            WHERE owned_id = {pk}
            UNION ALL
            SELECT s.id, s.owned_id, s.owner_id, s.stake
            FROM recursive_shareholders AS r, hold_stake AS s
            WHERE r.owner_id = s.owned_id 
            )
        SELECT DISTINCT * FROM recursive_shareholders
    """,
    }

    if key not in queries.keys():
        raise Exception(f"Invalid key <{key}> when attempting to run stake_raw_query")

    return queries[key]
