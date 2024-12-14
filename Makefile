RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

all:
	mkdir -p build
	date --utc +%Y%m%d%H%M%S > VERSION
	${RPMBUILD} --define "_version %(cat VERSION)" -ba rockit-shtstick.spec
	${RPMBUILD} --define "_version %(cat VERSION)" -ba python3-rockit-shtstick.spec

	mv build/noarch/*.rpm .
	rm -rf build VERSION

install:
	@date --utc +%Y%m%d%H%M%S > VERSION
	@python3 -m build --outdir .
	@sudo pip3 install rockit.shtstick-$$(cat VERSION)-py3-none-any.whl
	@rm VERSION
	@cp shtstickd shtstick /bin/
	@cp shtstickd@.service /usr/lib/systemd/system/
	@cp completion/shtstick /etc/bash_completion.d/
	@install -d /etc/shtstickd
	@echo ""
	@echo "Installed server, client, and service files."
	@echo "Now copy the relevant json config files to /etc/shtstickd/"
	@echo "and udev rules to /usr/lib/udev/rules.d/"
