USE db_image_class;

-- This embed_dist fucntion is used for computing L2 distance of two embeddings
delimiter //
CREATE FUNCTION embed_dist (embed1 TEXT, embed2 TEXT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE sub_str CHAR(32);
    DECLARE decvalue INT;
    DECLARE floatvalue1 FLOAT DEFAULT 0;
    DECLARE floatvalue2 FLOAT DEFAULT 0;
    DECLARE diff FLOAT DEFAULT 0;
    DECLARE total_diff FLOAT DEFAULT 0;
    DECLARE done INTEGER DEFAULT 0;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    hex_loop: LOOP
        -- get two float values
        SET sub_str = SUBSTRING(embed1, i+2, 8);  -- 0x01234567 (remove top 0x prefix)
        SET decvalue = CONV(sub_str, 16, 10);
        SET floatvalue1 = SIGN(decvalue) *  (1.0 + (decvalue &  0x007FFFFF) * POWER(2.0, -23))  * POWER(2.0, (decvalue & 0x7f800000) / 0x00800000 - 127);
        -- SET floatvalue1 = hex_to_float(sub_str1);
        SET sub_str = SUBSTRING(embed2, i+2, 8);  -- 0x01234567 (remove top 0x prefix)
        SET decvalue = CONV(sub_str, 16, 10);
        SET floatvalue2 = SIGN(decvalue) *  (1.0 + (decvalue &  0x007FFFFF) * POWER(2.0, -23))  * POWER(2.0, (decvalue & 0x7f800000) / 0x00800000 - 127);
        -- compute its difference
        SET diff = POWER(floatvalue1 - floatvalue2, 2);
        SET total_diff = total_diff + diff;
        SET i = i + 10;
        IF i <= 512 * 10 THEN
            ITERATE hex_loop;
        END IF;
        LEAVE hex_loop;
    END LOOP hex_loop;

    RETURN total_diff;
END; //
delimiter ;

DROP FUNCTION embed_dist;
