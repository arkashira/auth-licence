# breakeven.md

## Unit Economics & Break-even Analysis

### Cost per Active User
- **Compute Cost:** $0.10/user/month (based on cloud service pricing for serverless functions)
- **Storage Cost:** $0.05/user/month (average storage cost for user data)
- **Bandwidth Cost:** $0.02/user/month (average bandwidth cost for API calls)

**Total Cost per Active User:**  
**= Compute Cost + Storage Cost + Bandwidth Cost**  
**= $0.10 + $0.05 + $0.02 = $0.17/user/month**

### Pricing Tiers
| Tier Name       | Price ($/mo) | Features                                                                 |
|------------------|--------------|--------------------------------------------------------------------------|
| **Basic**        | $9           | 1,000 authentications, Email support, Basic analytics                   |
| **Pro**          | $29          | 10,000 authentications, Priority support, Advanced analytics, API access |
| **Enterprise**    | $99          | Unlimited authentications, Dedicated account manager, Custom features    |

### Customer Acquisition Cost (CAC) Range
- **Estimated CAC:** $50 - $100 per user (considering marketing, sales efforts, and onboarding costs)

### Lifetime Value (LTV) Estimate
- **Average Revenue per User (ARPU):** 
  - Basic: $9/month
  - Pro: $29/month
  - Enterprise: $99/month
- **Average Customer Lifespan:** 24 months (based on industry averages for SaaS)
  
**LTV Calculation:**
- **Basic Tier:** LTV = $9 * 24 = $216
- **Pro Tier:** LTV = $29 * 24 = $696
- **Enterprise Tier:** LTV = $99 * 24 = $2,376

### Break-even Users Count
- **Monthly Fixed Costs:** $2,000 (estimated operational and overhead costs)
  
**Break-even Users Count Calculation:**
- Break-even = Monthly Fixed Costs / (Price per User - Cost per User)

**For Basic Tier:**
- Break-even = $2,000 / ($9 - $0.17) = 238 users

**For Pro Tier:**
- Break-even = $2,000 / ($29 - $0.17) = 69 users

**For Enterprise Tier:**
- Break-even = $2,000 / ($99 - $0.17) = 20 users

### Path to $10K MRR
To achieve $10,000 Monthly Recurring Revenue (MRR):

**Basic Tier:**
- Required Users = $10,000 / $9 = 1,111 users

**Pro Tier:**
- Required Users = $10,000 / $29 = 345 users

**Enterprise Tier:**
- Required Users = $10,000 / $99 = 101 users

### Summary
- **Total Cost per Active User:** $0.17
- **Break-even Users Count:** 
  - Basic: 238
  - Pro: 69
  - Enterprise: 20
- **Path to $10K MRR:** 
  - Basic: 1,111 users
  - Pro: 345 users
  - Enterprise: 101 users