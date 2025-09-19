{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.python3Packages.qrcode
    pkgs.python3Packages.pillow
  ];
}
