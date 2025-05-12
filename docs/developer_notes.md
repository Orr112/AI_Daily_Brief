### ✅ API Routing Best Practices

**Always define route prefixes explicitly in your routers to ensure consistent API paths.**

#### Problem Encountered

The `/api/v1/health` endpoint was returning `{"detail": "Not Found"}` even though the health check route was defined in `health.py`.

#### Root Cause

The `APIRouter` in `health.py` was created without a prefix:

```python
router = APIRouter()
```

This caused the route to be registered at `/health` instead of `/api/v1/health`.

#### Solution

Update the router to explicitly include the correct prefix:

```python
router = APIRouter(prefix="/api/v1")
```

Alternatively, specify the prefix in the file where the router is included:

```python
router.include_router(health_router, prefix="/api/v1")
```

#### Best Practice

* Define route prefixes **inside each router module** to ensure they are self-contained and reusable.
* Keep route structure consistent with API versioning, e.g., `/api/v1/...`.
* Avoid relying solely on `include_router()` for setting important path structure unless necessary.

---

Include this pattern in all new router files to prevent confusion and broken endpoint paths.
