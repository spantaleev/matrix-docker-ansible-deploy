{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    agru-src = {
      url = "github:etkecc/agru";
      flake = false;
    };
  };
  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      agru-src,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        agru = pkgs.buildGo125Module {
          pname = "agru";
          version = "0.1.19";
          src = agru-src;
          vendorHash = null;
        };
      in
      with pkgs;
      {
        devShells.default = mkShell {
          buildInputs = [
            just
            ansible
            agru
          ];
          shellHook = ''
            echo "$(ansible --version)"
          '';
        };
      }
    );
}
