from config import field_sizes, config
import checker.new_check as checker

def test_sizes():
    assert field_sizes.cell_height * config.ver_cell_amt == field_sizes.field_height
    assert field_sizes.cell_width * config.hor_cell_amt == field_sizes.field_width


def test_checker():
    assert checker.check_word("море")
    assert not checker.check_word("сонце")
