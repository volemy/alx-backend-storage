-- sql script that creates a stored procedure computeAverageWeightedScoreForUser
-- that computes and stores the average weighted score for a student
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
  DECLARE total_weight FLOAT DEFAULT 0;
  DECLARE total_score FLOAT DEFAULT 0;

  -- Reset user's average score
  UPDATE users SET average_score = 0 WHERE id = user_id;

  -- Compute weighted score for each project
  SELECT SUM(projects.weight * corrections.score) INTO total_score, SUM(projects.weight) INTO total_weight
  FROM corrections
  JOIN projects ON corrections.project_id = projects.id
  WHERE corrections.user_id = user_id;

  -- Update user's average score
  UPDATE users SET average_score = total_score / total_weight WHERE id = user_id;
END$$

DELIMITER ;
