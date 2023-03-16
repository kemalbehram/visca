local config = import 'default.jsonnet';

config {
  'visca_9000-1'+: {
    validators: super.validators[0:1] + [{
      name: 'fullnode',
    }],
  },
}
