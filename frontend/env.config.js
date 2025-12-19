require('dotenv').config();

module.exports = function (env) {
  return {
    SUPABASE_URL: env.SUPABASE_URL || process.env.SUPABASE_URL || '',
    SUPABASE_ANON_KEY: env.SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY || ''
  };
};
