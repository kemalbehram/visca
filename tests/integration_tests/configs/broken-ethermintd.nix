{ pkgs ? import ../../../nix { } }:
let viscad = (pkgs.callPackage ../../../. { });
in
viscad.overrideAttrs (oldAttrs: {
  patches = oldAttrs.patches or [ ] ++ [
    ./broken-viscad.patch
  ];
})
