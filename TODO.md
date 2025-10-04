# TODO

## Implementation

- [ ] `/timezones` endpoint
    - [x] return all timezones
    - [ ] cache extracted timezones
    - [ ] Remove 'uninhabited'
    - [ ] sort timezones alphabetically
    - [ ] Add nautical timezones returned for uninhabited coordinates
    - [ ] Docs
- [ ] `/timezones?lat=y&lon=x`
    - [ ] Use `GeoDataFrame.cx` for coordinate lookup
    - [x] Verify coordinates (`pydantic` model?)
    - [ ] Return timezone for 'uninhabited' coordinates: Use nautical definition (1h/15° longitude). Use `Etc/GMT` with reversed signs!
    - [ ] Oceans are not covered: Use nautical rules.
    - [ ] Docs
- Production service
    - [ ] copy code/data in `Dockerfile`
    - [ ] `Dockerfile` command: run service
    - [ ] `README.md` & Service docs
    - [ ] smoketest (`curl`) for final image.
    - [ ] Healthcheck

## Other
- [ ] Load data using fastAPI lifespan events
- [ ] Setup stubs for mypy
