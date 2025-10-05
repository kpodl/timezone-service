# TODO

## Implementation

- [x] `/timezones` endpoint
    - [x] return all timezones
    - [x] cache extracted timezones
    - [x] Remove 'uninhabited'
    - [x] sort timezones alphabetically
    - [x] Add nautical timezones returned for uninhabited coordinates
    - [x] Docs
- [x] `/timezones?lat=y&lon=x`
    - [x] Use `GeoDataFrame.sindex.query()` for coordinate lookup
    - [x] Verify coordinates (`pydantic` model?)
    - [x] Return timezone for 'uninhabited' coordinates: Use nautical definition (1h/15° longitude). Use `Etc/GMT` with reversed signs!
    - [x] Oceans are not covered: Use nautical rules.
    - [x] Docs
- Production service
    - [x] copy code/data in `Dockerfile`
    - [x] `Dockerfile` command: run service
    - [x] `README.md` & Service docs
    - [x] smoketest (`curl`) for final image.
    - [x] Healthcheck

## Other
- [ ] Load data using fastAPI lifespan events
- [x] Setup stubs for mypy
