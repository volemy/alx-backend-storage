-- Sql script that Create an expression-based index on the first letter of the 'name' column
CREATE INDEX idx_name_first ON names(name(1));
