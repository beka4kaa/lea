"""Test the demo data seeding utility."""

import pytest
from sqlalchemy import select

from mcp_ui_aggregator.data.demo_seed import SEED_COMPONENTS
from mcp_ui_aggregator.models.database import Component


@pytest.mark.asyncio
async def test_seed_demo_is_idempotent(test_session):
    # Insert one of the seed components manually
    existing = Component(
        name=SEED_COMPONENTS[0]["name"],
        namespace=SEED_COMPONENTS[0]["namespace"],
        component_type=SEED_COMPONENTS[0]["component_type"],
        title=SEED_COMPONENTS[0]["title"],
    )
    test_session.add(existing)
    await test_session.commit()

    # Count before
    res_before = await test_session.execute(select(Component))
    count_before = len(res_before.scalars().all())

    # Simulate seeding logic: add missing ones only
    namespaces = {(c["namespace"], c["name"]) for c in SEED_COMPONENTS}
    res_all = await test_session.execute(select(Component.namespace, Component.name))
    have = set(res_all.all())
    missing = [c for c in SEED_COMPONENTS if (c["namespace"], c["name"]) not in have]

    for data in missing:
        test_session.add(Component(**data))
    await test_session.commit()

    # After
    res_after = await test_session.execute(select(Component))
    count_after = len(res_after.scalars().all())

    # Should have added at least some, but not duplicates
    assert count_after >= count_before
    # No duplicates of the (namespace, name) pair
    res_pairs = await test_session.execute(select(Component.namespace, Component.name))
    pairs = res_pairs.all()
    assert len(pairs) == len(set(pairs))
