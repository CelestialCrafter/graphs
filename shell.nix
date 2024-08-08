with import <nixpkgs> { };
mkShell {
  packages = [
    (python3.withPackages (
      python-pkgs: with python-pkgs; [
        matplotlib
        yapf
        numpy
        pykakasi
      ]
    ))
  ];
}
