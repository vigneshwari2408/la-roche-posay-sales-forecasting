# Data Model — Star Schema

Designed to support BI reporting for La Roche-Posay's multi-channel retail operations.

## Fact Tables

| Table | Grain | Key Metrics |
|---|---|---|
| `fact_sales` | One row per sale | `quantity`, `total_amount` |
| `fact_orders` | One row per order | `total_order_value`, `order_status` |
| `fact_inventory` | One row per product/date | `stock_level` |
| `fact_reviews` | One row per review | `rating`, `review_text` |
| `fact_campaign` | One row per channel/date | `clicks`, `conversions` |

## Dimension Tables

| Table | Description |
|---|---|
| `dim_customer` | Customer profile incl. skin type and country |
| `dim_product` | Product catalogue with category and skin concern |
| `dim_date` | Date spine with day, month, year attributes |
| `dim_channel` | Sales channel (Website, Pharmacy, Mobile App, Amazon, Clinic) |
| `dim_location` | Market geography (France, Germany, UK, Spain, Italy) |

## Schema Diagram

```
                    dim_date
                       │
dim_customer ──── fact_sales ──── dim_product
                       │
dim_channel ───────────┤
                       │
dim_location ──────────┘
```

## Design Decisions

- **Slowly Changing Dimensions**: `dim_customer` uses `created_at` to support SCD Type 2 if needed
- **Skin type segmentation**: Enables product recommendation analysis by customer skin profile
- **Multi-channel**: `dim_channel` allows campaign ROI to be tied back to sales performance via shared date and channel keys
