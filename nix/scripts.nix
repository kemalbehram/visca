{ pkgs
, config
, visca ? (import ../. { inherit pkgs; })
}: rec {
  start-visca = pkgs.writeShellScriptBin "start-visca" ''
    # rely on environment to provide viscad
    export PATH=${pkgs.test-env}/bin:$PATH
    ${../scripts/start-visca.sh} ${config.visca-config} ${config.dotenv} $@
  '';
  start-geth = pkgs.writeShellScriptBin "start-geth" ''
    export PATH=${pkgs.test-env}/bin:${pkgs.go-ethereum}/bin:$PATH
    source ${config.dotenv}
    ${../scripts/start-geth.sh} ${config.geth-genesis} $@
  '';
  start-scripts = pkgs.symlinkJoin {
    name = "start-scripts";
    paths = [ start-visca start-geth ];
  };
}
