
build:
	zip -r -j ./build/symbols-anki_v21.zip symbols

clean:
	rm -rf ./build/*

test: testclean
	cp -r ./symbols ~/.local/share/Anki2/addons21/symbols-test
	anki

testclean:
	rm -rf ~/.local/share/Anki2/addons21/symbols-test