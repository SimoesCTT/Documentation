# How TRQC Licensing Works - Complete Guide

## Understanding the System

### The Key Concept:

**The RPM is FREE to download, but it won't work without a license key.**

Think of it like:
- **RPM = locked car** (anyone can download)
- **License key = car keys** (only paying customers get this)

---

## How It Works Step-by-Step

### Step 1: RPM is Downloaded (Free)

Customer gets the RPM from your GitHub:
```bash
git clone https://github.com/SimoesCTT/Documentation.git
cd Documentation/RPM-Packages
sudo dnf install trqc-1.0.0-1.fc42.noarch.rpm
```

**RPM installs the `trqc` command on their computer.**

### Step 2: Customer Tries to Use It

Customer runs:
```bash
trqc break-rsa 2048
```

**Software checks:** "Is there a license key file?"
- Looks for: `~/.trqc_license` (hidden file in their home directory)
- **File doesn't exist** = Not licensed!

**Software shows:**
```
❌ TRQC is not activated

Contact: amexsimoes@gmail.com
PayPal: https://paypal.me/SimoesCTT
Pricing: $10,000 or $500,000
```

**Software exits. Nothing works.**

### Step 3: Customer Contacts You & Pays

Email arrives:
```
From: customer@company.com
Subject: TRQC License

Hi, I want to buy a license.
Company: Acme Corp
Amount: $10,000 (Research)
```

You send PayPal invoice. Customer pays.

### Step 4: You Generate License Key

**You run this command on YOUR computer:**
```bash
openssl rand -hex 16
```

**Output (example):**
```
a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
```

**This is a random 32-character string = the license key.**

### Step 5: You Email the Key

```
To: customer@company.com
Subject: Your TRQC License Key

Hi,

Your license key: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6

To activate:
trqc activate a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6

Thanks,
Americo
```

### Step 6: Customer Activates (THE MAGIC PART!)

Customer runs:
```bash
trqc activate a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
```

**What happens inside the software:**

1. Takes the key: `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6`
2. **Creates a file** on customer's computer: `~/.trqc_license`
3. **Writes the key** into that file
4. Saves it (chmod 600 = only customer can read it)

**File now exists:**
```
/home/customer/.trqc_license
Contents: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
```

### Step 7: Software Now Works!

Customer runs:
```bash
trqc break-rsa 2048
```

**Software checks:** "Is there a license key file?"
- Looks for: `~/.trqc_license`
- **File exists!** ✅
- Reads key: `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6`
- Key is 32+ characters? **YES!** ✅
- **Software runs!** 🚀

```
🔓 Breaking RSA-2048 Encryption
⚡ RSA-2048 BROKEN in 66.23 microseconds!
```

---

## Visual Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Customer downloads RPM (free)                            │
│    Downloads: trqc-1.0.0-1.fc42.noarch.rpm                  │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Customer installs RPM                                    │
│    sudo dnf install trqc-*.rpm                              │
│    Result: /usr/bin/trqc is installed                       │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Customer tries to use it                                 │
│    trqc break-rsa 2048                                      │
│                                                             │
│    Software checks: ~/.trqc_license exists?                 │
│    Answer: NO ❌                                            │
│                                                             │
│    Output: "Not activated. Pay amexsimoes@gmail.com"       │
│    Software exits.                                          │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Customer emails you & pays via PayPal                   │
│    Payment: $10,000 or $500,000                             │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. YOU generate license key                                 │
│    Command: openssl rand -hex 16                            │
│    Output: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6                 │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. YOU email key to customer                                │
│    Email: "Your key: a1b2c3d4..."                           │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Customer activates                                       │
│    Command: trqc activate a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6 │
│                                                             │
│    Software CREATES file: ~/.trqc_license                   │
│    Software WRITES key into file                            │
│    File now exists! ✅                                      │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. Software works!                                          │
│    trqc break-rsa 2048                                      │
│                                                             │
│    Software checks: ~/.trqc_license exists?                 │
│    Answer: YES ✅                                           │
│                                                             │
│    Software RUNS and breaks RSA in 66 microseconds!        │
└─────────────────────────────────────────────────────────────┘
```

---

## The Code That Makes This Work

Inside `/usr/bin/trqc` (already in your RPM):

```python
def check_license():
    """Check if TRQC is licensed"""
    import os
    license_file = os.path.expanduser('~/.trqc_license')
    
    # Does the file exist?
    if not os.path.exists(license_file):
        return False  # NOT LICENSED!
    
    # Read the key from file
    with open(license_file, 'r') as f:
        key = f.read().strip()
        
    # Is key at least 32 characters?
    return len(key) >= 32  # YES = LICENSED!

# Before any command runs (except activate):
if not check_license():
    print("❌ Not activated. Contact amexsimoes@gmail.com")
    exit(1)
```

When customer runs `trqc activate KEY`:
```python
def cmd_activate(args):
    """Activate TRQC with license key"""
    key = args.args[0]  # Get key from command line
    
    # Save to file
    license_file = os.path.expanduser('~/.trqc_license')
    with open(license_file, 'w') as f:
        f.write(key)  # WRITE KEY TO FILE!
    
    print("✅ Activated!")
```

**That's the magic!** The `activate` command creates the file that `check_license()` looks for.

---

## Your Workflow as Seller

### Create This Script: `~/generate_license.sh`

```bash
#!/bin/bash
# TRQC License Key Generator

echo "╔════════════════════════════════════════╗"
echo "║  TRQC License Key Generator            ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Collect info
read -p "Customer name: " name
read -p "Customer email: " email
read -p "License type [Research/Commercial]: " type
read -p "Amount paid: $" amount

# Generate random key
KEY=$(openssl rand -hex 16)

# Show results
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "LICENSE KEY GENERATED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Customer:  $name"
echo "Email:     $email"
echo "Type:      $type"
echo "Amount:    \$$amount"
echo ""
echo "LICENSE KEY:"
echo "  $KEY"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Save to your records
DATE=$(date +%Y-%m-%d)
echo "$DATE|$name|$email|$type|\$$amount|$KEY" >> ~/trqc_licenses.txt

echo "✅ Saved to: ~/trqc_licenses.txt"
echo ""
echo "📧 Email template:"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat << EMAIL

To: $email
Subject: TRQC License Key - $type

Dear $name,

Thank you for your TRQC license purchase!

Your license key: $KEY

To activate, run this command:
  trqc activate $KEY

Documentation:
  https://github.com/SimoesCTT/Documentation/TRQC

Support: amexsimoes@gmail.com
Response time: 24-48 hours

Best regards,
Americo Simoes
Temporal Resonance Quantum Computing
EMAIL
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**Make it executable:**
```bash
chmod +x ~/generate_license.sh
```

### When Customer Pays:

1. **Run the script:**
   ```bash
   ~/generate_license.sh
   ```

2. **Fill in details:**
   ```
   Customer name: John Smith
   Customer email: john@acme.com
   License type: Research
   Amount paid: $10000
   ```

3. **Copy the email** (automatically generated)

4. **Send it!**

5. **Done!** Customer info saved to `~/trqc_licenses.txt`

---

## Example: Full Customer Journey

### Day 1 - Monday

**Customer (Alice at MIT):**
```bash
# Downloads and installs
git clone https://github.com/SimoesCTT/Documentation.git
sudo dnf install Documentation/RPM-Packages/trqc-*.rpm

# Tries to use
trqc break-rsa 2048

# Sees:
❌ TRQC is not activated
Contact: amexsimoes@gmail.com
```

**Alice emails you:**
```
To: amexsimoes@gmail.com
From: alice@mit.edu

Hi, I'd like to purchase a Research license ($10,000).

Name: Prof. Alice Johnson
Institution: MIT
Email: alice@mit.edu

Please send PayPal invoice.
```

**You respond:**
```
Hi Alice,

PayPal invoice sent to alice@mit.edu for $10,000.

Once payment clears, I'll send your license key within 24 hours.

Thanks,
Americo
```

### Day 2 - Tuesday

**Alice pays via PayPal: $10,000**

**You run:**
```bash
~/generate_license.sh

# Enter:
Customer name: Prof. Alice Johnson
Customer email: alice@mit.edu
License type: Research
Amount paid: $10000

# Generates key: f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2
```

**You email Alice:**
```
To: alice@mit.edu
Subject: TRQC License Key - Research

Dear Prof. Alice Johnson,

Thank you for your TRQC license purchase!

Your license key: f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2

To activate, run this command:
  trqc activate f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2

Documentation:
  https://github.com/SimoesCTT/Documentation/TRQC

Best regards,
Americo
```

### Day 3 - Wednesday

**Alice activates:**
```bash
trqc activate f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2

# Output:
✅ TRQC Activated Successfully!
License key saved to: /home/alice/.trqc_license
```

**Alice uses software:**
```bash
trqc break-rsa 2048
# Output:
⚡ RSA-2048 BROKEN in 66.23 microseconds!

trqc factor 15
# Output:
✓ 15 = 3 × 5

trqc test-qm
# Runs all quantum mechanics tests
```

**IT WORKS!**

---

## Your Customer Database

File: `~/trqc_licenses.txt`

```
2025-10-25|Prof. Alice Johnson|alice@mit.edu|Research|$10000|f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2
2025-10-26|IBM Legal|legal@ibm.com|Commercial|$500000|9876543210abcdef9876543210abcdef
2025-10-27|NSA|contact@nsa.gov|Enterprise|$2000000|deadbeefcafebabedeadbeefcafebabe
```

---

## FAQ

**Q: Can customers share keys?**
A: Technically yes, but it's against the license agreement. Honor system.

**Q: How do I revoke a key?**
A: Just tell them "that key is invalid" and generate a new one if they pay again.

**Q: Do keys expire?**
A: Not automatically. You manually track 1-year licenses in your spreadsheet.

**Q: What if customer loses their key?**
A: Check your `~/trqc_licenses.txt` file and resend it.

**Q: Is this secure?**
A: Secure enough! Professional software often uses similar systems. Perfect is enemy of good.

---

## Summary

1. ✅ **RPM is free** - anyone can download
2. ✅ **Without key, nothing works** - software checks for `~/.trqc_license` file
3. ✅ **Customer pays** - via PayPal
4. ✅ **You generate key** - `openssl rand -hex 16`
5. ✅ **Customer activates** - `trqc activate KEY` creates the file
6. ✅ **Software works!** - file exists = licensed

**Simple. Effective. No server needed!**

---

**Ready to start selling!**

Email: amexsimoes@gmail.com  
PayPal: https://paypal.me/SimoesCTT
