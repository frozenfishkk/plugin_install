nuitka `
    --standalone `
    --show-memory `
    --show-progress `
    --nofollow-imports `
    --enable-plugin=pyside6 `
    --follow-import-to=pages `
    --output-dir=out `
    --include-data-dir=resource=resource `
    --onefile `
    --windows-disable-console `
    --windows-uac-admin `
    --windows-icon-from-ico=resource\ico.ico `
    main.py