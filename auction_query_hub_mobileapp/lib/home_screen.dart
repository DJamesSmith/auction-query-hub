import 'package:auction_query_hub_mobileapp/add_user.dart';
import 'package:flutter/material.dart';

import 'users_list.dart';
import 'auction_form.dart';
import 'users_list.dart';
import 'auctions_list.dart';
import 'analytics.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  void openPage(BuildContext context, Widget page) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => page,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 20),
            const Text('Welcome to', style: TextStyle(fontSize: 18, color: Colors.grey)),
            const SizedBox(height: 4),
            const Text(
              'Auction Query Hub',
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                letterSpacing: -0.5,
              ),
            ),
            const SizedBox(height: 12),
            const Text(
              'Manage users, auctions and analytics from one place.',
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey,
                height: 1.5,
              ),
            ),
      
            const SizedBox(height: 35),
      
            const Text(
              'Quick Actions',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
      
            const SizedBox(height: 16),
      
            Row(
              children: [
      
                Expanded(
                  child: _ActionCard(
                    icon: Icons.person_add_alt_1,
                    title: 'Add User',
                    subtitle: 'Create a new user',
                    onTap: () {
                      openPage(
                        context,
                        const AddUser(),
                      );
                    },
                  ),
                ),
      
                const SizedBox(width: 16),
      
                Expanded(
                  child: _ActionCard(
                    icon: Icons.gavel,
                    title: 'Add Auction',
                    subtitle: 'Create an auction',
                    onTap: () {
                      openPage(
                        context,
                        const AuctionForm(),
                      );
                    },
                  ),
                ),
              ],
            ),
      
            const SizedBox(height: 35),
      
            const Text(
              'Explore',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
      
            const SizedBox(height: 16),
      
            _NavigationCard(
              icon: Icons.people_outline,
              title: 'Users',
              subtitle: 'View and manage registered users',
              onTap: () {
                openPage(
                  context,
                  const UsersList(),
                );
              },
            ),
      
            const SizedBox(height: 14),
      
            _NavigationCard(
              icon: Icons.gavel_outlined,
              title: 'Auctions',
              subtitle: 'Browse available auction items',
              onTap: () {
                openPage(
                  context,
                  const AuctionsList(),
                );
              },
            ),
      
            const SizedBox(height: 14),
      
            _NavigationCard(
              icon: Icons.analytics_outlined,
              title: 'Analytics',
              subtitle: 'View auction and user insights',
              onTap: () {
                openPage(
                  context,
                  const Analytics(),
                );
              },
            ),
      
            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }
}


class _ActionCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _ActionCard({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(18),

      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(18),

        child: Padding(
          padding: const EdgeInsets.all(20),

          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [

              Icon(
                icon,
                size: 32,
                color: Theme.of(context).colorScheme.primary,
              ),

              const SizedBox(height: 18),

              Text(
                title,
                style: const TextStyle(
                  fontSize: 17,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 5),

              Text(
                subtitle,
                style: const TextStyle(
                  fontSize: 13,
                  color: Colors.grey,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}


class _NavigationCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _NavigationCard({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(18),

      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(18),

        child: Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: 20,
            vertical: 18,
          ),

          child: Row(
            children: [

              Container(
                padding: const EdgeInsets.all(12),

                decoration: BoxDecoration(
                  color: Theme.of(context)
                      .colorScheme
                      .primary
                      .withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(12),
                ),

                child: Icon(
                  icon,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),

              const SizedBox(width: 16),

              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,

                  children: [

                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 4),

                    Text(
                      subtitle,
                      style: const TextStyle(
                        fontSize: 14,
                        color: Colors.grey,
                      ),
                    ),
                  ],
                ),
              ),

              const Icon(
                Icons.chevron_right,
                color: Colors.grey,
              ),
            ],
          ),
        ),
      ),
    );
  }
}