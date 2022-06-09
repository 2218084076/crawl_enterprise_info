"""Test main"""
import pytest

from runer import (company_link_task, main, main_category_tesk, parse_task,
                   rollback_task)


@pytest.mark.asyncio
async def test_main(mocker):
    """Test main"""
    mock_main = mocker.patch.object(main)
    mock_main_category_tesk = mocker.patch.object(main_category_tesk)
    mock_rollback_task = mocker.patch.object(rollback_task)
    mock_parse_task = mocker.patch.object(parse_task)
    mock_company_link_task = mocker.patch.object(company_link_task)
    mock_main()
    mock_rollback_task.assert_called()
    mock_company_link_task.assert_called()
    mock_parse_task.assert_called()
    mock_main_category_tesk.assert_called()
