addon_dir := `echo ~/.local/share/Anki2/addons21/symbols-test`

build:
    mkdir -p ./build
    zip -r -j ./build/symbols-anki_v21.zip symbols

clean:
    rm -rf ./build

test: testclean
    cp -r ./symbols {{ addon_dir }}
    anki

testclean:
    rm -rf {{ addon_dir }}
