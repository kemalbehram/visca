local config = import 'default.jsonnet';

config {
  'visca_9000-1'+: {
    'app-config'+: {
      'minimum-gas-prices': '100000000000aphoton',
    },
    genesis+: {
      app_state+: {
        feemarket+: {
          params+: {
            base_fee:: super.base_fee,
          },
        },
      },
    },
  },
}
