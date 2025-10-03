# TODO

## Implementation

- [ ] `/timezones` endpoint
  - [x] return all timezones
  - [ ] cache extracted timezones
  - [ ] Remove 'uninhabited'
- [ ] `/timezones?lat=y&lon=x`
  - [ ] Use `GeoDataFrame.cx` for coordinate lookup
  - [ ] Verify coordinates (`pydantic` model?)
- [ ] Return timezone for 'uninhabited' coordinates: Use nautical definition (1h/15° longitude)

## Other
- [ ] Setup stubs for mypy
- [ ] copy code/data in `Dockerfile`
- [ ] `Dockerfile` command: run service
- [ ] smoketest (`curl`) for final image.
- [ ] `README.md`
