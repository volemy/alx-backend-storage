-- Script that creates a trigger that decreases the quantity of an item after adding a new order
-- Quantity in the table items can be negative
DELIMITER $$

-- Drop existing trigger if it exists
DROP TRIGGER IF EXISTS after_order_reduction $$

-- Create a new trigger
CREATE TRIGGER after_order_reduction
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END $$

DELIMITER ;
