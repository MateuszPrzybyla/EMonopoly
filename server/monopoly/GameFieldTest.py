import unittest
from server.monopoly.GameField import GameField
from utils.eMonopoly import Field, FieldType, FieldColor

__author__ = 'mateusz'


class CityFieldTests(unittest.TestCase):
    def setUp(self):
        self.cityModel = Field(1, "Pole", FieldType.CITY, FieldColor.GREEN,
                               value=200, fees=[10, 20, 30, 40, 50, 60], houseCost=50)
        self.cityModelTwo = Field(2, "Pole 2", FieldType.CITY, FieldColor.GREEN,
                                  value=300, fees=[10, 20, 30, 40, 50, 60], houseCost=50)
        self.cityModelOther = Field(3, "Pole 3", FieldType.CITY, FieldColor.RED,
                                    value=400, fees=[10, 20, 30, 40, 50, 60], houseCost=100)
        self.cityField = GameField(self.cityModel)
        self.cityFieldTwo = GameField(self.cityModelTwo)
        self.fieldSet = [self.cityField, self.cityFieldTwo]
        self.cityField.fieldSet = self.fieldSet

    def test_monopolized_success(self):
        self.cityField.owner = 2
        self.cityFieldTwo.owner = 2
        self.assertTrue(self.cityField.isMonopolized(), 'city is monopolized if color owned by the same owner')

    def test_monopolized_fail_no_owner(self):
        self.cityField.owner = 2
        self.assertFalse(self.cityField.isMonopolized(), 'city is not monopolized if other city not owned')

    def test_monopolized_fail_other_owner(self):
        self.cityField.owner = 2
        self.cityFieldTwo.owner = 3
        self.assertFalse(self.cityField.isMonopolized(), 'city is not monopolized if other city owned by others')

    def test_monopolized_fail_no_owners(self):
        self.assertFalse(self.cityField.isMonopolized(), 'city is not monopolized if no city in color is owned')

    def test_fee_no_owner(self):
        self.assertEqual(0, self.cityField.getFee(10), 'fee should be zero when no owner')

    def test_fee_no_houses_basic(self):
        self.cityField.houses = 0
        self.cityField.owner = 2
        self.assertEqual(10, self.cityField.getFee(10), 'fee should be the lowest possible when owned with no houses')

    def test_fee_no_houses_monopolized(self):
        self.cityField.houses = 0
        self.cityField.owner = 2
        self.cityFieldTwo.owner = 2
        self.assertEqual(20, self.cityField.getFee(10), 'fee should be the double when monopolized')

    def test_fee_with_two_houses(self):
        self.cityField.houses = 2
        self.cityField.owner = 2
        self.assertEqual(30, self.cityField.getFee(10), 'fee should be taken from house related fees')

    def test_fee_with_hotel(self):
        self.cityField.houses = 5
        self.cityField.owner = 2
        self.assertEqual(60, self.cityField.getFee(10), 'fee should be taken from hotel related fee')

    def test_fee_wrong_houses(self):
        self.cityField.houses = 6
        self.cityField.owner = 2
        self.assertEqual(0, self.cityField.getFee(10), 'fee should be 0 for wrong houses amount')

    def test_associated_fields(self):
        self.assertEqual([self.cityField, self.cityFieldTwo], self.cityField.getAssociatedFields(),
                         'all fields with the same color should be associated')

    def test_associated_fields_skipping_owners(self):
        self.cityField.owner = 1
        self.cityFieldTwo.owner = 2
        self.assertEqual([self.cityField, self.cityFieldTwo], self.cityField.getAssociatedFields(),
                         'all fields with the same color should be associated, even with different owners')

    def test_can_build_house_success(self):
        self.cityField.owner = 1
        self.cityField.mortgage = False
        self.cityFieldTwo.owner = 1
        self.assertTrue(self.cityField.canBuildHouse(1),
                        'should be able to build house when is the owner of all associated fields and no mortgage')

    def test_cannot_build_house_when_no_monopoly(self):
        self.cityField.owner = 1
        self.cityField.mortgage = False
        self.cityFieldTwo.owner = 2
        self.assertFalse(self.cityField.canBuildHouse(1),
                         'should not be able to build house when is not the owner of all associated fields')

    def test_cannot_build_house_when_mortgage(self):
        self.cityField.owner = 1
        self.cityField.mortgage = True
        self.cityFieldTwo.owner = 1
        self.assertFalse(self.cityField.canBuildHouse(1), 'should not be able to build house when field is mortgaged')

    def test_cannot_build_house_when_other_associated_field_mortgaged(self):
        self.cityField.owner = 1
        self.cityField.mortgage = False
        self.cityFieldTwo.owner = 1
        self.cityFieldTwo.mortgage = True
        self.assertFalse(self.cityField.canBuildHouse(1), 'should not be able to build house when field is mortgaged')

    def test_cannot_build_house_when_too_much_discrepancy(self):
        self.cityField.owner = 1
        self.cityFieldTwo.owner = 1
        self.cityField.houses = 1
        self.cityFieldTwo.houses = 0
        self.assertFalse(self.cityField.canBuildHouse(1),
                         'should not be able to build house when there is discrepancy between number of houses')

    def test_can_build_house_when_number_of_houses_even(self):
        self.cityField.owner = 1
        self.cityFieldTwo.owner = 1
        self.cityField.houses = 3
        self.cityFieldTwo.houses = 3
        self.assertTrue(self.cityField.canBuildHouse(1),
                        'should be able to build house when there is even number of houses on all fields')

    def test_cannot_build_house_when_already_has_hotel(self):
        self.cityField.owner = 1
        self.cityFieldTwo.owner = 1
        self.cityField.houses = 5
        self.assertFalse(self.cityField.canBuildHouse(1), 'should not be able to build house when there is a hotel')

    def test_can_destroy_house_success(self):
        self.cityField.owner = 1
        self.cityFieldTwo.owner = 1
        self.cityField.houses = 4
        self.cityFieldTwo.houses = 4
        self.assertTrue(self.cityField.canSellHouse(1), 'should be able to sell house')

    def test_can_destroy_house_even_when_no_monopol(self):
        self.cityField.owner = 1
        self.cityField.houses = 4
        self.assertTrue(self.cityField.canSellHouse(1),
                        'should be able to sell house even when does not own all fields')

    def test_can_destroy_hotel(self):
        self.cityField.owner = 1
        self.cityField.houses = 5
        self.assertTrue(self.cityField.canSellHouse(1), 'should be able to sell hotel')

    def test_cannot_destroy_house_when_too_much_discrepancy(self):
        self.cityField.owner = 1
        self.cityField.houses = 4
        self.cityFieldTwo.owner = 1
        self.cityFieldTwo.houses = 5
        self.assertFalse(self.cityField.canSellHouse(1),
                         'should not be able to sell house when there is too much discrepancy between number of houses')

    def test_sell_house_value_zero(self):
        self.cityField.houses = 0
        self.assertEqual(0, self.cityField.sellHouse(), 'value should be zero when no houses built')
        self.assertEqual(0, self.cityField.houses, 'there should be still zero houses')

    def test_sell_house_value_non_zero(self):
        self.cityField.houses = 3
        self.assertEqual(25, self.cityField.sellHouse(), 'value should be half of actual houses price')
        self.assertEqual(2, self.cityField.houses, 'there should be two houses after sell')

    def test_clear_house_value_non_zero(self):
        self.cityField.houses = 3
        self.assertEqual(75, self.cityField.clearHouses(), 'value should be half of actual houses price of all houses')
        self.assertEqual(0, self.cityField.houses, 'there should be no houses after sell')

    def test_mortgage_success(self):
        self.cityField.owner = 1
        self.cityField.houses = 0
        self.assertTrue(self.cityField.canDoMortgage(1), 'owner should be able to mortgage field if no houses built')

    def test_mortgage_already_mortgaged(self):
        self.cityField.owner = 1
        self.cityField.mortgage = True
        self.assertFalse(self.cityField.canDoMortgage(1), 'owner should not be able to mortgage again')

    def test_mortgage_houses(self):
        self.cityField.owner = 1
        self.cityField.houses = 1
        self.assertFalse(self.cityField.canDoMortgage(1), 'owner should not be able to mortgage field if houses > 0')

    def test_mortgage_houses_on_other_field(self):
        self.cityField.owner = 1
        self.cityFieldTwo.houses = 1
        self.assertFalse(self.cityField.canDoMortgage(1),
                         'owner should not be able to mortgage field if there are houses on other associated fields')

    def test_mortgage_other_owner(self):
        self.cityField.owner = 2
        self.cityField.houses = 1
        self.assertFalse(self.cityField.canDoMortgage(1), 'owner should be able to mortgage someone others field')

    def test_mortgage_value(self):
        self.cityField.owner = 2
        self.cityField.houses = 0
        self.assertEqual(100, self.cityField.getMortgageSellValue(), 'mortgage value should be half the price')

    def test_lift_mortgage_success(self):
        self.cityField.owner = 2
        self.cityField.mortgage = True
        self.assertTrue(self.cityField.canLiftMortgage(2), 'owner can lift the mortgage')

    def test_lift_mortgage_other_owner(self):
        self.cityField.owner = 1
        self.cityField.mortgage = True
        self.assertFalse(self.cityField.canLiftMortgage(2), 'mortgage cannot be lifted by non-owner')

    def test_lift_mortgage_not_mortgaged(self):
        self.cityField.owner = 2
        self.cityField.mortgage = False
        self.assertFalse(self.cityField.canLiftMortgage(2), 'mortgage cannot be lifted if not mortgaged')

    def test_lift_mortgage_value(self):
        self.assertEqual(110, self.cityField.getMortgageBuyValue(),
                         'mortgage lift value should be 110% of mortgage price')