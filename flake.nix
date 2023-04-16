{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs, ... }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in
    {
      devShell.x86_64-linux = pkgs.mkShell {
        buildInputs = with pkgs; [
          just
          python311Packages.ansible-core
          python311Packages.passlib
        ];
        LC_ALL = "C.UTF-8";
        LC_CTYPE = "C.UTF-8";
      };
    };
}
