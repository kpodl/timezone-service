# TODO

## Implementation

- [ ] `/timezones` endpoint
    - [x] return all timezones
    - [x] cache extracted timezones
    - [x] Remove 'uninhabited'
    - [x] sort timezones alphabetically
    - [x] Add nautical timezones returned for uninhabited coordinates
    - [ ] Docs
- [ ] `/timezones?lat=y&lon=x`
    - [x] Use `GeoDataFrame.sindex.query()` for coordinate lookup
    - [x] Verify coordinates (`pydantic` model?)
    - [x] Return timezone for 'uninhabited' coordinates: Use nautical definition (1h/15° longitude). Use `Etc/GMT` with reversed signs!
    - [x] Oceans are not covered: Use nautical rules.
    - [ ] Docs
- Production service
    - [ ] copy code/data in `Dockerfile`
    - [ ] `Dockerfile` command: run service
    - [ ] `README.md` & Service docs
    - [ ] smoketest (`curl`) for final image.
    - [ ] Healthcheck

## Other
- [ ] Load data using fastAPI lifespan events
- [x] Setup stubs for mypy
