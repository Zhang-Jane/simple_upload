
/**
 * 是否是开发环境
 */

export const IS_DEV = false;

export const DEVELOPMENT = "http://127.0.0.1:9011/api/v1"; // 开发环境
export const PRODUCTION = "http://192.168.100.10:80/api/v1"; // 线上环境
export const BACKEND_BASE_URL = IS_DEV ? DEVELOPMENT : PRODUCTION;