CREATE TABLE IF NOT EXISTS "DmacCenter" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  -- 设备 mac地址
  "d_mac" text DEFAULT '',
  -- 设备外网地址
  "d_host" text DEFAULT '',
  -- 设备序列号码
  "d_uuid" text DEFAULT '',
  -- 设备程序日期
  "d_date" text DEFAULT '',
  -- 设备加密类型
  "d_type" text DEFAULT '',
  -- 设备所属区域
  "d_area" text DEFAULT ''
);
