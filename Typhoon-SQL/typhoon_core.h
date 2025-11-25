#ifndef TYPHOON_CORE_H
#define TYPHOON_CORE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <time.h>
#include <math.h>

// ============================================================================
// TYPHOON CTT-ENHANCED PRECISION STRIKE PARAMETERS
// ============================================================================

// CTT Constants - borrowed from TEMPEST for stealth
#define ALPHA 0.0302
#define RESONANCE_KILL 587000      // Death frequency
#define RESONANCE_STEALTH 293500   // Stealth frequency
#define PI_TEMPORAL 1.2294
#define G_TEMPORAL 1.0222

// Prime resonance for kill shot timing
extern int kill_primes[4];

// Strike modes - single precision hits
#define STRIKE_SURGICAL    0x01    // One precise kill
#define STRIKE_RESONANT    0x02    // CTT-amplified strike  
#define STRIKE_STEALTH     0x04    // Invisible kill
#define STRIKE_CRITICAL    0x08    // Hit critical weakness

// ============================================================================
// TYPHOON CONFIGURATION STRUCTURE
// ============================================================================

typedef struct {
    char target[256];           // Target URL for attack
    unsigned char strike_mode;  // Single strike mode
    int use_ctt_stealth;        // Use CTT temporal cloaking
    int resonance_amplified;    // Amplify with resonance frequency
    int critical_hit;           // Target critical system weakness
    double kill_frequency;      // Calculated optimal kill frequency
} TyphoonConfig;

// ============================================================================
// CTT PHYSICS ENGINE FOR PRECISION STRIKES
// ============================================================================

/**
 * Calculate optimal kill frequency using CTT
 * Returns the exact frequency to collapse target's temporal framework
 */
double calculate_kill_frequency(TyphoonConfig *config);

/**
 * Calculate critical weakness in target using resonance analysis
 * Identifies the single point of failure
 */
const char* identify_critical_weakness(TyphoonConfig *config);

/**
 * Apply CTT temporal cloaking to hide strike
 * Uses negative resonance to make attack invisible
 */
void apply_ctt_stealth(TyphoonConfig *config);

/**
 * Amplify payload with resonance frequency
 * Single payload becomes exponentially more destructive
 */
char* amplify_with_resonance(const char *base_payload, double frequency);

// ============================================================================
// PRECISION STRIKE VECTORS - ONE HIT KILLS
// ============================================================================

/**
 * Single surgical strike - one payload, total destruction
 */
void typhoon_surgical_strike(TyphoonConfig *config);

/**
 * Resonant kill - CTT-amplified single hit
 */
void typhoon_resonant_kill(TyphoonConfig *config);

/**
 * Stealth assassination - invisible single strike
 */
void typhoon_stealth_kill(TyphoonConfig *config);

/**
 * Critical strike - hit the one weak point
 */
void typhoon_critical_strike(TyphoonConfig *config);

// ============================================================================
// PRECISION EXECUTION ENGINE
// ============================================================================

/**
 * Execute single precision strike with CTT timing
 * Waits for exact prime resonance moment, then strikes once
 */
void execute_precision_strike(const char *sql, TyphoonConfig *config);

/**
 * Wait for optimal kill window using CTT calculations
 */
void wait_for_kill_window(double frequency);

// ============================================================================
// SYSTEM MANAGEMENT
// ============================================================================

/**
 * Initialize typhoon weapon system
 */
void init_typhoon_system(void);

/**
 * Cleanup typhoon resources
 */
void cleanup_typhoon_system(void);

/**
 * Deploy typhoon weapon with specified configuration
 */
void deploy_typhoon_weapon(TyphoonConfig *config);

/**
 * Parse command line arguments for typhoon
 */
TyphoonConfig parse_typhoon_arguments(int argc, char *argv[]);

/**
 * Verify single-strike kill success
 */
void verify_one_hit_kill(TyphoonConfig *config);

#endif // TYPHOON_CORE_H
